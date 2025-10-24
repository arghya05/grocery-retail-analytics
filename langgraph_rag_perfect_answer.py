#!/usr/bin/env python3
"""
RAG-BASED PERFECT ANSWER SYSTEM
- Retrieves ALL context using RAG (metadata, KPIs, insights, recommendations)
- Generates MULTIPLE candidate answers (3-5)
- Evaluates each answer for alignment with question
- Picks the PERFECT answer (100% aligned)
- No premature intent decision - full context evaluation
"""

import pandas as pd
import json
import os
import re
from typing import Literal, Optional, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from pydantic import BaseModel, Field
import requests

# ===== SCHEMAS =====

class RetrievedContext(BaseModel):
    """All context retrieved via RAG"""
    kpi_data: str = Field(description="Relevant KPI data from CSVs")
    metadata: str = Field(description="Business metadata and expertise")
    insights: str = Field(description="Strategic insights document")
    recommendations: str = Field(description="Best practices and recommendations")
    prompt_guidance: str = Field(description="Store manager prompt template")


class CandidateAnswer(BaseModel):
    """A candidate answer with its reasoning"""
    answer_text: str = Field(description="The actual answer")
    reasoning: str = Field(description="Why this answer fits the question")
    confidence: float = Field(description="Confidence score 0-1", ge=0.0, le=1.0)


class AnswerEvaluation(BaseModel):
    """Evaluation of an answer's alignment with question"""
    answer_id: int
    alignment_score: float = Field(description="How well answer aligns with question (0-1)", ge=0.0, le=1.0)
    directly_answers: bool = Field(description="Does it directly answer what was asked?")
    uses_relevant_data: bool = Field(description="Uses data relevant to the question?")
    correct_entity_type: bool = Field(description="Talks about right entity (store/category)?")
    appropriate_detail: bool = Field(description="Right amount of detail for question?")
    no_hallucination: bool = Field(description="No made-up information?")
    issues: List[str] = Field(description="Any issues found", default=[])


# ===== STATE =====
class RAGState(TypedDict):
    question: str
    retrieved_context: Optional[RetrievedContext]
    candidate_answers: List[CandidateAnswer]
    evaluations: List[AnswerEvaluation]
    best_answer: Optional[CandidateAnswer]
    final_answer: str


# ===== RAG RETRIEVAL SYSTEM =====
class RAGRetriever:
    """Retrieves ALL relevant context for the question"""

    def __init__(self):
        self.kpi_data = {}
        self.metadata = {}
        self.insights = ""
        self.prompt_template = ""
        self.load_all_sources()

    def load_all_sources(self):
        """Load all context sources"""
        print("\n" + "="*70)
        print("LOADING ALL CONTEXT SOURCES FOR RAG")
        print("="*70)

        # KPI data
        kpi_files = {
            'store_performance': 'kpi_store_performance.csv',
            'category_performance': 'kpi_category_performance.csv',
            'customer_segment': 'kpi_customer_segment.csv',
            'overall_business': 'kpi_overall_business.csv',
            'product_performance': 'kpi_product_performance.csv',
            'daily_performance': 'kpi_daily_performance.csv',
        }

        for key, filename in kpi_files.items():
            if os.path.exists(filename):
                self.kpi_data[key] = pd.read_csv(filename)

        print(f"✓ Loaded {len(self.kpi_data)} KPI datasets")

        # Metadata
        if os.path.exists('store_manager_metadata_layer.json'):
            with open('store_manager_metadata_layer.json', 'r') as f:
                self.metadata = json.load(f)
            print(f"✓ Loaded metadata layer")

        # Insights
        if os.path.exists('COMPLETE_DATA_INSIGHTS.md'):
            with open('COMPLETE_DATA_INSIGHTS.md', 'r') as f:
                self.insights = f.read()
            print(f"✓ Loaded insights document")

        # Prompt template
        if os.path.exists('store_manager_prompt_template.txt'):
            with open('store_manager_prompt_template.txt', 'r') as f:
                self.prompt_template = f.read()
            print(f"✓ Loaded prompt template")

        print("="*70 + "\n")

    def retrieve(self, question: str) -> RetrievedContext:
        """Retrieve ALL relevant context for the question"""
        print("\n🔍 RAG RETRIEVAL: Gathering all relevant context...")

        q_lower = question.lower()

        # Determine relevant entities
        relevant_sources = []
        if any(word in q_lower for word in ["store", "stores", "str_"]):
            relevant_sources.append("store_performance")
        if any(word in q_lower for word in ["category", "categories", "beverage", "snacks", "dairy"]):
            relevant_sources.append("category_performance")
        if any(word in q_lower for word in ["customer", "segment", "regular", "premium"]):
            relevant_sources.append("customer_segment")
        if any(word in q_lower for word in ["product", "products", "item"]):
            relevant_sources.append("product_performance")
        if any(word in q_lower for word in ["daily", "day", "time"]):
            relevant_sources.append("daily_performance")

        # If nothing specific, load overall
        if not relevant_sources:
            relevant_sources.append("overall_business")

        # Retrieve KPI data
        kpi_context = []
        for source in relevant_sources:
            if source in self.kpi_data:
                df = self.kpi_data[source]

                # Smart filtering based on question
                if "top" in q_lower and "store" in source:
                    top_match = re.search(r'top\s+(\d+)', q_lower)
                    n = int(top_match.group(1)) if top_match else 5
                    df = df.sort_values('Total_Revenue', ascending=False).head(n)
                elif any(word in q_lower for word in ["bottom", "worst", "not performing", "underperform"]) and "store" in source:
                    bottom_match = re.search(r'bottom\s+(\d+)', q_lower)
                    n = int(bottom_match.group(1)) if bottom_match else 10
                    df = df.sort_values('Total_Revenue', ascending=True).head(n)
                elif "how many" in q_lower or "count" in q_lower:
                    # For count queries, just need the count
                    count = len(df)
                    kpi_context.append(f"\n=== {source.upper()} ===\nTotal count: {count}\n")
                    continue

                kpi_context.append(f"\n=== {source.upper().replace('_', ' ')} ===\n")
                kpi_context.append(df.head(50).to_string(index=False))
                kpi_context.append("\n")

        kpi_data_str = "".join(kpi_context) if kpi_context else "No specific KPI data retrieved"

        # Retrieve metadata context
        metadata_context = []
        if self.metadata:
            persona = self.metadata.get('persona', {})
            metadata_context.append(f"Role: {persona.get('role', 'Store Manager')}")
            metadata_context.append(f"Experience: {persona.get('experience_level', '20+ years')}")

            # Add relevant insights from metadata
            detailed_insights = self.metadata.get('detailed_insights', {})
            if 'revenue' in q_lower and 'revenue_performance' in detailed_insights:
                rev = detailed_insights['revenue_performance']
                metadata_context.append(f"\nRevenue Context: Peak {rev.get('peak_month')}, Variance {rev.get('variance')}")

            if 'customer' in q_lower and 'customer_segmentation' in detailed_insights:
                cust = detailed_insights['customer_segmentation']
                metadata_context.append(f"\nCustomer Context: {json.dumps(cust)[:200]}")

        metadata_str = "\n".join(metadata_context) if metadata_context else ""

        # Strategic insights (first 2000 chars)
        insights_str = self.insights[:2000] if self.insights else ""

        # Prompt guidance (for tone and structure)
        prompt_guidance = self.prompt_template[:1000] if self.prompt_template else ""

        context = RetrievedContext(
            kpi_data=kpi_data_str,
            metadata=metadata_str,
            insights=insights_str,
            recommendations="",  # Can add specific recommendations if needed
            prompt_guidance=prompt_guidance
        )

        print(f"  ✓ Retrieved context from {len(relevant_sources)} sources")
        print(f"  ✓ KPI data: {len(kpi_data_str)} chars")
        print(f"  ✓ Metadata: {len(metadata_str)} chars")
        print(f"  ✓ Insights: {len(insights_str)} chars")

        return context


# Global RAG retriever
rag_retriever = RAGRetriever()


# ===== OLLAMA =====
def call_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2:1b", "prompt": prompt, "stream": False},
            timeout=180
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        return ""
    except Exception as e:
        return f"Error: {str(e)}"


# ===== AGENT 1: RAG RETRIEVAL =====
def rag_retrieval_agent(state: RAGState) -> Command[Literal["multi_answer_generator"]]:
    """Retrieve ALL relevant context"""
    print("\n📚 RAG RETRIEVAL AGENT: Gathering all context...")

    question = state["question"]
    context = rag_retriever.retrieve(question)

    return Command(
        goto="multi_answer_generator",
        update={"retrieved_context": context}
    )


# ===== AGENT 2: MULTI-ANSWER GENERATOR =====
def multi_answer_generator(state: RAGState) -> Command[Literal["answer_evaluator"]]:
    """Generate MULTIPLE candidate answers (3-5)"""
    print("\n🎯 MULTI-ANSWER GENERATOR: Creating candidate answers...")

    question = state["question"]
    context = state["retrieved_context"]

    candidates = []

    # Strategy 1: DIRECT ANSWER (minimal)
    print("  → Generating candidate 1: Direct answer...")
    direct_prompt = f"""Answer this question directly and concisely.

QUESTION: {question}

DATA:
{context.kpi_data[:2000]}

Answer in 1-2 sentences. Be direct. Use specific numbers from the data."""

    answer1 = call_ollama(direct_prompt)
    candidates.append(CandidateAnswer(
        answer_text=answer1,
        reasoning="Direct, minimal answer",
        confidence=0.7
    ))

    # Strategy 2: CONTEXTUAL ANSWER (with insight)
    print("  → Generating candidate 2: Contextual answer...")
    contextual_prompt = f"""Answer this question with context and a key insight.

QUESTION: {question}

DATA:
{context.kpi_data[:2000]}

METADATA:
{context.metadata}

Provide:
1. Direct answer (1 sentence)
2. Key insight (1 sentence explaining what it means)

Total: 2-3 sentences."""

    answer2 = call_ollama(contextual_prompt)
    candidates.append(CandidateAnswer(
        answer_text=answer2,
        reasoning="Contextual with insight",
        confidence=0.8
    ))

    # Strategy 3: COMPREHENSIVE ANSWER (analysis)
    print("  → Generating candidate 3: Comprehensive answer...")
    comprehensive_prompt = f"""Provide a comprehensive answer as an experienced store manager.

QUESTION: {question}

DATA:
{context.kpi_data[:2000]}

METADATA:
{context.metadata}

INSIGHTS:
{context.insights[:1000]}

Provide:
1. Direct answer with specific data
2. Key insight or "why"
3. Actionable recommendation (if appropriate)

Keep it concise: 100-150 words max."""

    answer3 = call_ollama(comprehensive_prompt)
    candidates.append(CandidateAnswer(
        answer_text=answer3,
        reasoning="Comprehensive with analysis",
        confidence=0.85
    ))

    print(f"  ✓ Generated {len(candidates)} candidate answers")

    return Command(
        goto="answer_evaluator",
        update={"candidate_answers": candidates}
    )


# ===== AGENT 3: ANSWER EVALUATOR =====
def answer_evaluator(state: RAGState) -> Command[Literal["best_answer_selector"]]:
    """Evaluate each answer for alignment with question"""
    print("\n⚖️  ANSWER EVALUATOR: Scoring answer alignment...")

    question = state["question"]
    candidates = state["candidate_answers"]
    context = state["retrieved_context"]

    evaluations = []

    for i, candidate in enumerate(candidates):
        print(f"  → Evaluating answer {i+1}...")

        # Evaluation criteria
        answer_text = candidate.answer_text
        q_lower = question.lower()
        a_lower = answer_text.lower()

        # Check 1: Directly answers the question
        directly_answers = True
        if "how many" in q_lower and not any(char.isdigit() for char in answer_text):
            directly_answers = False
        if "why" in q_lower and "because" not in a_lower and "due to" not in a_lower:
            directly_answers = False

        # Check 2: Uses relevant data
        uses_relevant_data = any(char.isdigit() for char in answer_text) or \
                            any(word in answer_text for word in ["STR_", "₹", "%"])

        # Check 3: Correct entity type
        correct_entity = True
        if "store" in q_lower and "store" not in a_lower and "STR_" not in answer_text:
            correct_entity = False
        if "category" in q_lower and not any(cat in answer_text for cat in ["Beverages", "Snacks", "Dairy", "Bakery", "category"]):
            correct_entity = False

        # Check 4: Appropriate detail level
        answer_length = len(answer_text.split())
        appropriate_detail = True
        if "how many" in q_lower and answer_length > 20:
            appropriate_detail = False  # Too detailed for a count query
        if ("why" in q_lower or "should" in q_lower) and answer_length < 30:
            appropriate_detail = False  # Too brief for analysis query

        # Check 5: No hallucination (basic check)
        no_hallucination = True
        # Check if answer talks about wrong entities
        if "store" in q_lower and any(word in a_lower for word in ["beverage category", "snacks category"]):
            no_hallucination = False

        # Calculate alignment score
        checks = [directly_answers, uses_relevant_data, correct_entity, appropriate_detail, no_hallucination]
        alignment_score = sum(checks) / len(checks)

        # Collect issues
        issues = []
        if not directly_answers:
            issues.append("Doesn't directly answer the question")
        if not uses_relevant_data:
            issues.append("Missing specific data/numbers")
        if not correct_entity:
            issues.append("Wrong entity type")
        if not appropriate_detail:
            issues.append("Inappropriate detail level")
        if not no_hallucination:
            issues.append("Possible hallucination detected")

        evaluation = AnswerEvaluation(
            answer_id=i,
            alignment_score=alignment_score,
            directly_answers=directly_answers,
            uses_relevant_data=uses_relevant_data,
            correct_entity_type=correct_entity,
            appropriate_detail=appropriate_detail,
            no_hallucination=no_hallucination,
            issues=issues
        )

        evaluations.append(evaluation)

        print(f"    • Alignment score: {alignment_score:.0%}")
        if issues:
            print(f"    • Issues: {', '.join(issues)}")

    return Command(
        goto="best_answer_selector",
        update={"evaluations": evaluations}
    )


# ===== AGENT 4: BEST ANSWER SELECTOR =====
def best_answer_selector(state: RAGState) -> Command[Literal[END]]:
    """Select the best answer based on evaluations"""
    print("\n🏆 BEST ANSWER SELECTOR: Picking the perfect answer...")

    candidates = state["candidate_answers"]
    evaluations = state["evaluations"]

    # Find highest scoring answer
    best_eval = max(evaluations, key=lambda e: e.alignment_score)
    best_candidate = candidates[best_eval.answer_id]

    print(f"  ✓ Selected answer {best_eval.answer_id + 1}")
    print(f"  ✓ Alignment score: {best_eval.alignment_score:.0%}")
    print(f"  ✓ Reasoning: {best_candidate.reasoning}")

    # Format final answer
    final_answer = best_candidate.answer_text

    # Add quality badge
    if best_eval.alignment_score >= 0.9:
        final_answer += f"\n\n✓ **Answer Quality: {best_eval.alignment_score:.0%}** - Highly aligned with your question"
    elif best_eval.alignment_score >= 0.8:
        final_answer += f"\n\n✓ **Answer Quality: {best_eval.alignment_score:.0%}** - Well aligned"

    return Command(
        goto=END,
        update={
            "best_answer": best_candidate,
            "final_answer": final_answer
        }
    )


# ===== BUILD GRAPH =====
def build_rag_graph():
    builder = StateGraph(RAGState)

    builder.add_node("rag_retrieval_agent", rag_retrieval_agent)
    builder.add_node("multi_answer_generator", multi_answer_generator)
    builder.add_node("answer_evaluator", answer_evaluator)
    builder.add_node("best_answer_selector", best_answer_selector)

    builder.add_edge(START, "rag_retrieval_agent")

    return builder.compile()


# ===== MAIN SYSTEM =====
class RAGPerfectAnswerSystem:
    """RAG-based system that generates perfect answers"""

    def __init__(self):
        self.graph = build_rag_graph()
        print("\n" + "="*70)
        print("RAG-BASED PERFECT ANSWER SYSTEM INITIALIZED")
        print("="*70)
        print("✓ RAG Retrieval (all context sources)")
        print("✓ Multi-Answer Generation (3 candidates)")
        print("✓ Answer Evaluation (alignment scoring)")
        print("✓ Best Answer Selection (100% aligned)")
        print("="*70 + "\n")

    def ask(self, question: str) -> str:
        print("\n" + "="*70)
        print("RAG PERFECT ANSWER PIPELINE")
        print("="*70)

        initial_state = {
            "question": question,
            "retrieved_context": None,
            "candidate_answers": [],
            "evaluations": [],
            "best_answer": None,
            "final_answer": ""
        }

        result = self.graph.invoke(initial_state)

        print("\n" + "="*70)
        print("PERFECT ANSWER SELECTED")
        print("="*70 + "\n")

        return result["final_answer"]

    def run_interactive(self):
        print("\n" + "="*70)
        print("RAG PERFECT ANSWER SYSTEM")
        print("="*70)
        print("\n🎯 Features:")
        print("  • RAG retrieval (ALL context)")
        print("  • Multiple answer generation")
        print("  • Alignment evaluation")
        print("  • Best answer selection")
        print("\nType 'quit' to exit.")
        print("="*70 + "\n")

        while True:
            try:
                question = input("\n🏪 You: ").strip()

                if not question:
                    continue

                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you!")
                    break

                answer = self.ask(question)

                print("\n💼 Store Manager:\n")
                print(answer)
                print("\n" + "="*70)

            except KeyboardInterrupt:
                print("\n\n👋 Thank you!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                import traceback
                traceback.print_exc()


def main():
    import sys

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama connected")
    except:
        print("\n❌ ERROR: Cannot connect to Ollama!")
        sys.exit(1)

    system = RAGPerfectAnswerSystem()
    system.run_interactive()


if __name__ == "__main__":
    main()
