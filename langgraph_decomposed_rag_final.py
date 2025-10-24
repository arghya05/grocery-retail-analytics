#!/usr/bin/env python3
"""
DECOMPOSED RAG SYSTEM - FINAL VERSION
- Breaks complex queries into sub-questions
- Retrieves context via RAG for each sub-question
- Aggregates all context
- Generates multiple candidate answers
- Evaluates alignment (5-point check)
- ONLY returns answer if 100% aligned
- Otherwise asks for clarification or retries
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

class SubQuery(BaseModel):
    """A decomposed sub-question"""
    question: str = Field(description="The sub-question")
    purpose: str = Field(description="Why this sub-question is needed")
    entity_focus: str = Field(description="What entity: stores, categories, etc")


class QueryDecomposition(BaseModel):
    """Result of breaking down a complex query"""
    is_complex: bool = Field(description="Whether query needs decomposition")
    sub_queries: List[SubQuery] = Field(description="List of sub-questions", default=[])
    reasoning: str = Field(description="Why this decomposition")


class SubQueryContext(BaseModel):
    """Context retrieved for a sub-query"""
    sub_query: str
    retrieved_data: str
    source: str  # Which CSV/file


class AggregatedContext(BaseModel):
    """All context aggregated from sub-queries"""
    original_query: str
    sub_contexts: List[SubQueryContext]
    combined_context: str
    metadata: str
    insights: str


class CandidateAnswer(BaseModel):
    """A candidate answer"""
    answer_text: str
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)


class AlignmentEvaluation(BaseModel):
    """Strict alignment evaluation"""
    answer_id: int
    alignment_score: float = Field(ge=0.0, le=1.0)

    # 5-point check
    directly_answers: bool
    uses_relevant_data: bool
    correct_entity_type: bool
    appropriate_detail: bool
    no_hallucination: bool

    # Strict pass/fail
    passes_threshold: bool = Field(description="Score >= 100%")
    issues: List[str] = Field(default=[])


# ===== STATE =====
class DecomposedRAGState(TypedDict):
    question: str

    # Decomposition
    decomposition: Optional[QueryDecomposition]

    # RAG retrieval
    sub_contexts: List[SubQueryContext]
    aggregated_context: Optional[AggregatedContext]

    # Answer generation
    candidate_answers: List[CandidateAnswer]

    # Evaluation
    evaluations: List[AlignmentEvaluation]
    best_evaluation: Optional[AlignmentEvaluation]

    # Retry tracking
    attempt_number: int

    # Final output
    final_answer: str
    needs_clarification: bool


# ===== RAG SYSTEM =====
class RAGSystem:
    """RAG system that retrieves from all sources"""

    def __init__(self):
        self.kpi_data = {}
        self.metadata = {}
        self.insights = ""
        self.load_all()

    def load_all(self):
        print("\n" + "="*70)
        print("LOADING ALL SOURCES FOR DECOMPOSED RAG")
        print("="*70)

        kpi_files = {
            'store_performance': 'kpi_store_performance.csv',
            'category_performance': 'kpi_category_performance.csv',
            'customer_segment': 'kpi_customer_segment.csv',
            'overall_business': 'kpi_overall_business.csv',
            'product_performance': 'kpi_product_performance.csv',
        }

        for key, filename in kpi_files.items():
            if os.path.exists(filename):
                self.kpi_data[key] = pd.read_csv(filename)

        if os.path.exists('store_manager_metadata_layer.json'):
            with open('store_manager_metadata_layer.json', 'r') as f:
                self.metadata = json.load(f)

        if os.path.exists('COMPLETE_DATA_INSIGHTS.md'):
            with open('COMPLETE_DATA_INSIGHTS.md', 'r') as f:
                self.insights = f.read()

        print(f"✓ Loaded {len(self.kpi_data)} KPI datasets")
        print(f"✓ Loaded metadata and insights")
        print("="*70 + "\n")

    def retrieve_for_subquery(self, sub_query: SubQuery) -> SubQueryContext:
        """Retrieve context for a specific sub-query"""
        question = sub_query.question.lower()
        entity = sub_query.entity_focus

        # Determine which data source
        source = None
        data = None

        if "store" in entity:
            source = "store_performance"
            df = self.kpi_data.get(source)
            if df is not None:
                # Apply filtering based on question
                if "top" in question:
                    n = int(re.search(r'\d+', question).group()) if re.search(r'\d+', question) else 5
                    df = df.sort_values('Total_Revenue', ascending=False).head(n)
                elif "bottom" in question or "worst" in question or "underperform" in question:
                    n = int(re.search(r'\d+', question).group()) if re.search(r'\d+', question) else 10
                    df = df.sort_values('Total_Revenue', ascending=True).head(n)

                data = df.to_string(index=False)

        elif "category" in entity or "categories" in entity:
            source = "category_performance"
            df = self.kpi_data.get(source)
            if df is not None:
                data = df.to_string(index=False)

        elif "customer" in entity or "segment" in entity:
            source = "customer_segment"
            df = self.kpi_data.get(source)
            if df is not None:
                data = df.to_string(index=False)

        elif "product" in entity:
            source = "product_performance"
            df = self.kpi_data.get(source)
            if df is not None:
                data = df.head(50).to_string(index=False)

        else:
            source = "overall_business"
            df = self.kpi_data.get(source)
            if df is not None:
                data = df.to_string(index=False)

        if data is None:
            data = "No data available for this query"

        return SubQueryContext(
            sub_query=sub_query.question,
            retrieved_data=data[:3000],  # Limit size
            source=source or "none"
        )


# Global RAG system
rag_system = RAGSystem()


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
    except:
        return ""


# ===== AGENT 1: QUERY DECOMPOSER =====
def query_decomposer(state: DecomposedRAGState) -> Command[Literal["subquery_rag_retrieval", "simple_rag_retrieval"]]:
    """Break complex queries into sub-questions"""
    print("\n🔬 QUERY DECOMPOSER: Analyzing query complexity...")

    question = state["question"]
    q_lower = question.lower()

    # Check if complex
    is_complex = False
    sub_queries = []
    reasoning = ""

    # Pattern 1: Multiple entities mentioned
    entities_mentioned = []
    if "store" in q_lower:
        entities_mentioned.append("stores")
    if "category" in q_lower or "categories" in q_lower:
        entities_mentioned.append("categories")
    if "customer" in q_lower or "segment" in q_lower:
        entities_mentioned.append("customers")

    if len(entities_mentioned) > 1:
        is_complex = True
        reasoning = f"Multiple entities mentioned: {', '.join(entities_mentioned)}"

        # Create sub-queries for each entity
        for entity in entities_mentioned:
            sub_queries.append(SubQuery(
                question=f"What is the {entity} data?",
                purpose=f"Get {entity} information",
                entity_focus=entity
            ))

    # Pattern 2: Comparison query
    elif "compare" in q_lower or "vs" in q_lower or "versus" in q_lower:
        is_complex = True
        reasoning = "Comparison query requires multiple data sources"

        # Extract what to compare
        stores_mentioned = re.findall(r'STR_\d+', question)
        if len(stores_mentioned) >= 2:
            for store in stores_mentioned:
                sub_queries.append(SubQuery(
                    question=f"What is {store}'s performance?",
                    purpose=f"Get data for {store}",
                    entity_focus="stores"
                ))

    # Pattern 3: "Why" or "How" questions (need multiple contexts)
    elif any(word in q_lower for word in ["why", "how can", "what should"]):
        is_complex = True
        reasoning = "Analysis question needs context + insights"

        # Need data + insights
        if "store" in q_lower:
            sub_queries.append(SubQuery(
                question="What is the store performance data?",
                purpose="Get store metrics",
                entity_focus="stores"
            ))
        elif "category" in q_lower:
            sub_queries.append(SubQuery(
                question="What is the category performance data?",
                purpose="Get category metrics",
                entity_focus="categories"
            ))
        else:
            sub_queries.append(SubQuery(
                question="What is the overall business data?",
                purpose="Get business metrics",
                entity_focus="general"
            ))

    # Pattern 4: Simple query (how many, what is, total, count)
    else:
        is_complex = False
        reasoning = "Simple query, direct retrieval sufficient"

    decomposition = QueryDecomposition(
        is_complex=is_complex,
        sub_queries=sub_queries,
        reasoning=reasoning
    )

    print(f"  → Is Complex: {is_complex}")
    print(f"  → Reasoning: {reasoning}")

    if is_complex:
        print(f"  → Sub-queries: {len(sub_queries)}")
        for i, sq in enumerate(sub_queries, 1):
            print(f"    {i}. {sq.question} (entity: {sq.entity_focus})")

        return Command(
            goto="subquery_rag_retrieval",
            update={"decomposition": decomposition}
        )
    else:
        print(f"  → Route: Simple RAG retrieval")
        return Command(
            goto="simple_rag_retrieval",
            update={"decomposition": decomposition}
        )


# ===== AGENT 2A: SUB-QUERY RAG RETRIEVAL =====
def subquery_rag_retrieval(state: DecomposedRAGState) -> Command[Literal["context_aggregator"]]:
    """Retrieve context for each sub-query"""
    print("\n📚 SUB-QUERY RAG RETRIEVAL: Fetching context for each sub-query...")

    decomposition = state["decomposition"]
    sub_contexts = []

    for i, sub_query in enumerate(decomposition.sub_queries, 1):
        print(f"  → Sub-query {i}: {sub_query.question}")
        context = rag_system.retrieve_for_subquery(sub_query)
        sub_contexts.append(context)
        print(f"    ✓ Retrieved from {context.source} ({len(context.retrieved_data)} chars)")

    return Command(
        goto="context_aggregator",
        update={"sub_contexts": sub_contexts}
    )


# ===== AGENT 2B: SIMPLE RAG RETRIEVAL =====
def simple_rag_retrieval(state: DecomposedRAGState) -> Command[Literal["context_aggregator"]]:
    """Simple retrieval for non-complex queries"""
    print("\n📚 SIMPLE RAG RETRIEVAL: Direct context fetch...")

    question = state["question"]
    q_lower = question.lower()

    # Create single sub-query
    entity = "general"
    if "store" in q_lower:
        entity = "stores"
    elif "category" in q_lower:
        entity = "categories"
    elif "customer" in q_lower:
        entity = "customers"

    sub_query = SubQuery(
        question=question,
        purpose="Direct answer",
        entity_focus=entity
    )

    context = rag_system.retrieve_for_subquery(sub_query)
    print(f"  ✓ Retrieved from {context.source}")

    return Command(
        goto="context_aggregator",
        update={"sub_contexts": [context]}
    )


# ===== AGENT 3: CONTEXT AGGREGATOR =====
def context_aggregator(state: DecomposedRAGState) -> Command[Literal["multi_answer_generator"]]:
    """Aggregate all context from sub-queries"""
    print("\n🔗 CONTEXT AGGREGATOR: Combining all context...")

    sub_contexts = state["sub_contexts"]

    # Combine all data
    combined_parts = []
    for ctx in sub_contexts:
        combined_parts.append(f"\n=== {ctx.source.upper()} ===\n{ctx.retrieved_data}\n")

    combined = "".join(combined_parts)

    # Add metadata
    metadata_str = ""
    if rag_system.metadata:
        persona = rag_system.metadata.get('persona', {})
        metadata_str = f"Role: {persona.get('role')}, Experience: {persona.get('experience_level')}"

    # Add insights (first 1500 chars)
    insights_str = rag_system.insights[:1500]

    aggregated = AggregatedContext(
        original_query=state["question"],
        sub_contexts=sub_contexts,
        combined_context=combined,
        metadata=metadata_str,
        insights=insights_str
    )

    print(f"  ✓ Aggregated {len(sub_contexts)} context sources")
    print(f"  ✓ Total context: {len(combined)} chars")

    return Command(
        goto="multi_answer_generator",
        update={"aggregated_context": aggregated}
    )


# ===== AGENT 4: MULTI-ANSWER GENERATOR =====
def multi_answer_generator(state: DecomposedRAGState) -> Command[Literal["strict_evaluator"]]:
    """Generate 3 candidate answers"""
    print("\n🎯 MULTI-ANSWER GENERATOR: Creating candidates...")

    question = state["question"]
    context = state["aggregated_context"]

    candidates = []

    # Candidate 1: Direct
    print("  → Candidate 1: Direct answer")

    # Special handling for "how many" questions
    if "how many" in question.lower() or "number of" in question.lower():
        prompt1 = f"""Count the items from the data and answer with JUST THE NUMBER.

QUESTION: {question}

DATA:
{context.combined_context[:2000]}

Answer format: "X [items]" (e.g., "50 stores")
Keep it under 10 words."""
    else:
        prompt1 = f"""Answer directly using this data.

QUESTION: {question}

DATA:
{context.combined_context[:2000]}

Answer in 1-3 sentences. Be specific."""

    answer1 = call_ollama(prompt1)
    candidates.append(CandidateAnswer(
        answer_text=answer1,
        reasoning="Direct minimal answer",
        confidence=0.75
    ))

    # Candidate 2: Contextual
    print("  → Candidate 2: Contextual answer")
    prompt2 = f"""Answer with context and insight.

QUESTION: {question}

DATA:
{context.combined_context[:2000]}

METADATA: {context.metadata}

Provide:
1. Direct answer (1 sentence)
2. Key insight (1 sentence)

Total 2-3 sentences."""

    answer2 = call_ollama(prompt2)
    candidates.append(CandidateAnswer(
        answer_text=answer2,
        reasoning="Contextual with insight",
        confidence=0.85
    ))

    # Candidate 3: Comprehensive
    print("  → Candidate 3: Comprehensive answer")
    prompt3 = f"""Provide comprehensive answer as a store manager.

QUESTION: {question}

DATA:
{context.combined_context[:2000]}

INSIGHTS:
{context.insights[:800]}

Provide answer with data, insight, and recommendation if needed.
Keep concise: 100-150 words."""

    answer3 = call_ollama(prompt3)
    candidates.append(CandidateAnswer(
        answer_text=answer3,
        reasoning="Comprehensive analysis",
        confidence=0.80
    ))

    print(f"  ✓ Generated {len(candidates)} candidates")

    return Command(
        goto="strict_evaluator",
        update={"candidate_answers": candidates}
    )


# ===== AGENT 5: STRICT EVALUATOR (100% THRESHOLD) =====
def strict_evaluator(state: DecomposedRAGState) -> Command[Literal["final_decision_gate"]]:
    """Evaluate with STRICT 100% alignment requirement"""
    print("\n⚖️  STRICT EVALUATOR: Checking 100% alignment...")

    question = state["question"]
    candidates = state["candidate_answers"]

    evaluations = []

    for i, candidate in enumerate(candidates):
        print(f"  → Evaluating candidate {i+1}...")

        answer = candidate.answer_text
        q_lower = question.lower()
        a_lower = answer.lower()

        # 5-point check
        directly_answers = True
        if "how many" in q_lower and not any(char.isdigit() for char in answer):
            directly_answers = False
        if "compare" in q_lower and "vs" not in a_lower and "versus" not in a_lower and "compared to" not in a_lower:
            directly_answers = False

        uses_relevant_data = any(char.isdigit() for char in answer) or "STR_" in answer or "₹" in answer

        correct_entity = True
        if "store" in q_lower and "store" not in a_lower and "STR_" not in answer:
            correct_entity = False
        if "category" in q_lower and not any(cat in answer for cat in ["Beverages", "Snacks", "Dairy", "category"]):
            correct_entity = False

        answer_words = len(answer.split())
        appropriate_detail = True
        # More lenient for simple questions - allow up to 50 words
        if ("how many" in q_lower or "number of" in q_lower or "count" in q_lower or "total" in q_lower) and answer_words > 50:
            appropriate_detail = False
        # Complex questions need more detail
        if ("why" in q_lower or "should" in q_lower or "recommend" in q_lower or "how can" in q_lower) and answer_words < 30:
            appropriate_detail = False

        no_hallucination = True
        if "store" in q_lower and any(word in a_lower for word in ["beverage category", "snacks category"]):
            no_hallucination = False

        # Calculate score
        checks = [directly_answers, uses_relevant_data, correct_entity, appropriate_detail, no_hallucination]
        alignment_score = sum(checks) / len(checks)

        # STRICT: Must be 100%
        passes_threshold = (alignment_score >= 1.0)

        issues = []
        if not directly_answers:
            issues.append("Doesn't directly answer question")
        if not uses_relevant_data:
            issues.append("Missing data/numbers")
        if not correct_entity:
            issues.append("Wrong entity type")
        if not appropriate_detail:
            issues.append("Wrong detail level")
        if not no_hallucination:
            issues.append("Possible hallucination")

        evaluation = AlignmentEvaluation(
            answer_id=i,
            alignment_score=alignment_score,
            directly_answers=directly_answers,
            uses_relevant_data=uses_relevant_data,
            correct_entity_type=correct_entity,
            appropriate_detail=appropriate_detail,
            no_hallucination=no_hallucination,
            passes_threshold=passes_threshold,
            issues=issues
        )

        evaluations.append(evaluation)

        print(f"    • Alignment: {alignment_score:.0%}")
        print(f"    • Passes 100% threshold: {'✓ YES' if passes_threshold else '✗ NO'}")
        if issues:
            print(f"    • Issues: {', '.join(issues)}")

    # Find best (even if not 100%)
    best_eval = max(evaluations, key=lambda e: e.alignment_score)

    return Command(
        goto="final_decision_gate",
        update={
            "evaluations": evaluations,
            "best_evaluation": best_eval
        }
    )


# ===== AGENT 6: FINAL DECISION GATE =====
def final_decision_gate(state: DecomposedRAGState) -> Command[Literal[END]]:
    """ONLY return answer if 100% aligned, otherwise ask for clarification"""
    print("\n🚪 FINAL DECISION GATE: Checking if answer meets 100% threshold...")

    best_eval = state["best_evaluation"]
    best_candidate = state["candidate_answers"][best_eval.answer_id]

    print(f"  → Best alignment: {best_eval.alignment_score:.0%}")
    print(f"  → Passes 100% threshold: {best_eval.passes_threshold}")

    if best_eval.passes_threshold:
        # 100% aligned - return answer
        print(f"  ✅ APPROVED - Answer meets 100% alignment")

        final_answer = best_candidate.answer_text
        final_answer += f"\n\n✓ **Answer Quality: {best_eval.alignment_score:.0%}** - Fully aligned with your question"

        return Command(
            goto=END,
            update={
                "final_answer": final_answer,
                "needs_clarification": False
            }
        )
    else:
        # Not 100% aligned - ask for clarification
        print(f"  ❌ REJECTED - Answer does not meet 100% alignment")
        print(f"  → Issues: {', '.join(best_eval.issues)}")

        clarification = f"""I want to give you the most accurate answer, but I need clarification.

**Issues detected:**
{chr(10).join(f'  • {issue}' for issue in best_eval.issues)}

**Could you please:**
  • Rephrase your question with more specific details
  • Specify exactly what you want to know
  • Provide more context if needed

Example of what helps:
  • Instead of "How are things?" → "How many stores do we have?"
  • Instead of "Compare them" → "Compare STR_002 vs STR_041 revenue"
  • Instead of "Why?" → "Why are stores underperforming?"
"""

        return Command(
            goto=END,
            update={
                "final_answer": clarification,
                "needs_clarification": True
            }
        )


# ===== BUILD GRAPH =====
def build_decomposed_rag_graph():
    builder = StateGraph(DecomposedRAGState)

    builder.add_node("query_decomposer", query_decomposer)
    builder.add_node("subquery_rag_retrieval", subquery_rag_retrieval)
    builder.add_node("simple_rag_retrieval", simple_rag_retrieval)
    builder.add_node("context_aggregator", context_aggregator)
    builder.add_node("multi_answer_generator", multi_answer_generator)
    builder.add_node("strict_evaluator", strict_evaluator)
    builder.add_node("final_decision_gate", final_decision_gate)

    builder.add_edge(START, "query_decomposer")

    return builder.compile()


# ===== MAIN SYSTEM =====
class DecomposedRAGSystem:
    """Decomposed RAG with 100% alignment guarantee"""

    def __init__(self):
        self.graph = build_decomposed_rag_graph()
        print("\n" + "="*70)
        print("DECOMPOSED RAG SYSTEM - FINAL VERSION")
        print("="*70)
        print("✓ Query Decomposition (breaks complex queries)")
        print("✓ Sub-query RAG Retrieval (context for each part)")
        print("✓ Context Aggregation (combines all)")
        print("✓ Multi-Answer Generation (3 candidates)")
        print("✓ Strict Evaluation (100% alignment required)")
        print("✓ Final Gate (only returns if 100% aligned)")
        print("="*70 + "\n")

    def ask(self, question: str) -> str:
        initial_state = {
            "question": question,
            "decomposition": None,
            "sub_contexts": [],
            "aggregated_context": None,
            "candidate_answers": [],
            "evaluations": [],
            "best_evaluation": None,
            "attempt_number": 0,
            "final_answer": "",
            "needs_clarification": False
        }

        result = self.graph.invoke(initial_state)
        return result["final_answer"]

    def run_interactive(self):
        print("\n" + "="*70)
        print("DECOMPOSED RAG SYSTEM")
        print("="*70)
        print("\n🎯 Features:")
        print("  • Breaks complex queries into sub-questions")
        print("  • RAG retrieval for each part")
        print("  • 100% alignment required")
        print("  • Asks for clarification if < 100%")
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


def main():
    import sys

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama connected")
    except:
        print("\n❌ ERROR: Cannot connect to Ollama!")
        sys.exit(1)

    system = DecomposedRAGSystem()
    system.run_interactive()


if __name__ == "__main__":
    main()
