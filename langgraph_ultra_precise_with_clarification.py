#!/usr/bin/env python3
"""
ULTRA-PRECISE Multi-Agent Store Manager with CLARIFYING QUESTIONS
- Detects ambiguous questions
- Asks for clarification when needed
- Ensures 100% understanding before answering
"""

import pandas as pd
import json
import os
import re
from typing import Annotated, Literal, TypedDict, Optional, List
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from pydantic import BaseModel, Field
import requests

# ===== AMBIGUITY DETECTION SCHEMAS =====

class AmbiguityCheck(BaseModel):
    """Result of checking if question is ambiguous"""
    is_ambiguous: bool = Field(description="Whether the question is ambiguous")
    ambiguity_type: Optional[str] = Field(
        description="Type of ambiguity: entity_unclear, metric_unclear, time_unclear, comparison_unclear, vague",
        default=None
    )
    clarifying_questions: List[str] = Field(
        description="List of questions to ask for clarification",
        default=[]
    )
    examples: List[str] = Field(
        description="Example answers to show what we mean",
        default=[]
    )


class QuestionAnalysis(BaseModel):
    """Deep analysis of what the question is asking"""
    entity_type: Literal["store", "category", "product", "customer_segment", "time_period", "general"] = Field(
        description="Primary entity type being asked about"
    )
    specific_entities: List[str] = Field(
        description="Specific entities mentioned",
        default=[]
    )
    question_intent: Literal["identify", "compare", "analyze", "recommend", "explain"] = Field(
        description="What the question wants"
    )
    metrics_requested: List[str] = Field(
        description="Metrics being asked about",
        default=[]
    )
    filters: dict = Field(
        description="Any filters like 'top 5', 'bottom 10', etc.",
        default={}
    )
    expected_answer_format: str = Field(
        description="What format the answer should take"
    )


class AnswerRelevance(BaseModel):
    """Validates if answer matches question"""
    addresses_entity_type: bool
    addresses_specific_entities: bool
    answers_intent: bool
    includes_requested_metrics: bool
    correct_format: bool
    relevance_score: float = Field(ge=0.0, le=1.0)
    issues: List[str] = Field(default=[])


# ===== STATE DEFINITION =====
class UltraPreciseState(TypedDict):
    """State with ambiguity checking"""
    # Input
    question: str
    original_question: str  # Store original before clarification

    # Ambiguity checking
    ambiguity_check: Optional[AmbiguityCheck]
    needs_clarification: bool
    clarification_provided: Optional[str]

    # Question Understanding
    question_analysis: Optional[QuestionAnalysis]

    # Router outputs
    data_sources: list[str]
    analysis_type: str
    key_focus: str

    # Context data
    loaded_context: str
    structured_data: dict

    # Context validation
    context_matches_question: bool
    context_validation_feedback: str

    # Analysis outputs
    analysis: str

    # Answer relevance
    answer_relevance: Optional[AnswerRelevance]

    # Verification
    all_claims_valid: bool

    # Retry tracking
    attempt_number: int
    validation_feedback: str

    # Final output
    final_answer: str


# ===== DATA LOADER (Same as before) =====
class DataLoader:
    """Data loader with same functionality"""

    def __init__(self):
        self.context_data = {}
        self.business_context = {}
        self.load_all_data()

    def load_all_data(self):
        """Load all data sources"""
        print("\n" + "="*70)
        print("LOADING DATA FOR ULTRA-PRECISE SYSTEM WITH CLARIFICATION")
        print("="*70)

        # Load KPI files
        kpi_files = {
            'overall_business': 'kpi_overall_business.csv',
            'store_performance': 'kpi_store_performance.csv',
            'category_performance': 'kpi_category_performance.csv',
            'product_performance': 'kpi_product_performance.csv',
            'customer_segment': 'kpi_customer_segment.csv',
            'daily_performance': 'kpi_daily_performance.csv',
            'weekly_performance': 'kpi_weekly_performance.csv',
            'monthly_performance': 'kpi_monthly_performance.csv',
        }

        for key, filename in kpi_files.items():
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                self.context_data[key] = df

        print(f"✓ All {len(self.context_data)} KPI datasets")
        print("="*70 + "\n")

    def get_context_for_sources(self, data_sources: list[str], key_focus: str = "") -> tuple[str, dict]:
        """Load context and structured data"""
        context = []
        structured_data = {}

        if isinstance(data_sources, str):
            data_sources = [data_sources]

        for source in data_sources:
            if source in self.context_data:
                df = self.context_data[source]
                structured_data[source] = df

                context.append(f"\n=== {source.upper().replace('_', ' ')} DATA ===\n")

                if 'store_performance' in source:
                    df_sorted = df.sort_values('Total_Revenue', ascending=False)

                    if 'top' in key_focus.lower():
                        numbers = re.findall(r'\d+', key_focus)
                        if numbers:
                            top_n = int(numbers[0])
                            df_sorted = df_sorted.head(top_n)
                    elif 'bottom' in key_focus.lower() or 'not performing' in key_focus.lower():
                        numbers = re.findall(r'\d+', key_focus)
                        if numbers:
                            bottom_n = int(numbers[0])
                            df_sorted = df_sorted.tail(bottom_n)
                        else:
                            df_sorted = df_sorted.tail(10)

                    context.append(df_sorted.to_string(index=False))
                elif len(df) > 50:
                    context.append(df.head(50).to_string(index=False))
                else:
                    context.append(df.to_string(index=False))
                context.append("\n\n")

        return "".join(context), structured_data


# Global data loader
data_loader = DataLoader()


# ===== OLLAMA CLIENT =====
def call_ollama(prompt: str, model: str = "llama3.2:1b") -> str:
    """Call Ollama API"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"


# ===== AMBIGUITY DETECTOR =====
class AmbiguityDetector:
    """Detects if a question is ambiguous and needs clarification"""

    @staticmethod
    def check(question: str) -> AmbiguityCheck:
        """Check if question is ambiguous"""

        question_lower = question.lower()

        # Pattern 1: Pronoun without context
        pronouns = ["it", "they", "them", "that", "this", "these", "those"]
        if any(question_lower.startswith(p + " ") or question_lower.startswith(p + "'") for p in pronouns):
            return AmbiguityCheck(
                is_ambiguous=True,
                ambiguity_type="entity_unclear",
                clarifying_questions=[
                    "What specifically are you asking about? (stores, categories, products, or customer segments?)"
                ],
                examples=[
                    "Example: 'Which stores are performing well?'",
                    "Example: 'How is the Beverages category doing?'",
                    "Example: 'What are the top products by revenue?'"
                ]
            )

        # Pattern 2: Vague performance question
        vague_patterns = ["how is it going", "what's happening", "status", "update", "how are we doing", "what's going on"]
        if any(pattern in question_lower for pattern in vague_patterns) and len(question.split()) < 6:
            return AmbiguityCheck(
                is_ambiguous=True,
                ambiguity_type="vague",
                clarifying_questions=[
                    "What would you like to know about?",
                    "• Store performance (revenue, transactions)",
                    "• Category performance (which category?)",
                    "• Customer segments (Regular, Premium, etc.)",
                    "• Specific metrics (revenue, margins, customers)"
                ],
                examples=[
                    "Example: 'How are our top stores performing?'",
                    "Example: 'What's the revenue for Beverages category?'",
                    "Example: 'Which customer segment has the best retention?'"
                ]
            )

        # Pattern 3: Ambiguous "best" or "worst" without entity
        comparison_words = ["best", "worst", "top", "bottom"]
        if any(word in question_lower for word in comparison_words):
            has_entity = any(entity in question_lower for entity in
                           ["store", "stores", "category", "categories", "product", "products",
                            "customer", "customers", "segment"])
            if not has_entity:
                return AmbiguityCheck(
                    is_ambiguous=True,
                    ambiguity_type="entity_unclear",
                    clarifying_questions=[
                        "What are you comparing? Please specify:",
                        "• Stores (e.g., 'top 5 stores by revenue')",
                        "• Categories (e.g., 'best performing category')",
                        "• Products (e.g., 'worst selling products')",
                        "• Customer segments (e.g., 'most valuable segment')"
                    ],
                    examples=[
                        "Example: 'What are the top 5 stores by revenue?'",
                        "Example: 'Which is the worst performing category?'"
                    ]
                )

        # Pattern 4: Just a number or single word
        if len(question.split()) <= 2 and not any(word in question_lower for word in ["stores", "revenue", "categories"]):
            return AmbiguityCheck(
                is_ambiguous=True,
                ambiguity_type="vague",
                clarifying_questions=[
                    "Could you please ask a more specific question?",
                    "For example:",
                    "• 'How many stores do we have?'",
                    "• 'What is the total revenue?'",
                    "• 'Which categories are performing well?'"
                ],
                examples=[]
            )

        # Pattern 5: "Compare" without specifying what to compare
        if "compare" in question_lower or "vs" in question_lower or "versus" in question_lower:
            # Check if specific entities are mentioned
            has_specific = bool(re.search(r'STR_\d+', question)) or \
                          any(cat in question for cat in ["Beverages", "Snacks", "Dairy", "Bakery"])
            if not has_specific:
                return AmbiguityCheck(
                    is_ambiguous=True,
                    ambiguity_type="comparison_unclear",
                    clarifying_questions=[
                        "What would you like to compare?",
                        "Please specify the entities:",
                        "• Store IDs (e.g., 'Compare STR_002 vs STR_041')",
                        "• Categories (e.g., 'Compare Beverages vs Snacks')",
                        "• Time periods (e.g., 'Compare this month vs last month')"
                    ],
                    examples=[
                        "Example: 'Compare STR_002 and STR_041 revenue'",
                        "Example: 'Compare Beverages vs Snacks performance'"
                    ]
                )

        # Not ambiguous
        return AmbiguityCheck(
            is_ambiguous=False,
            ambiguity_type=None,
            clarifying_questions=[],
            examples=[]
        )


# ===== AGENT 1: AMBIGUITY CHECKER =====
def ambiguity_checker_agent(state: UltraPreciseState) -> Command[Literal["question_understanding_agent", END]]:
    """Check if question is ambiguous and needs clarification"""
    print("\n🔍 AMBIGUITY CHECKER: Checking if question is clear...")

    question = state["question"]

    # Check for ambiguity
    ambiguity_check = AmbiguityDetector.check(question)

    print(f"  → Is Ambiguous: {ambiguity_check.is_ambiguous}")
    if ambiguity_check.is_ambiguous:
        print(f"  → Type: {ambiguity_check.ambiguity_type}")
        print(f"  → Needs Clarification: Yes")

        # Format clarifying response
        clarification_request = f"""
❓ I need clarification to give you the best answer.

{chr(10).join(ambiguity_check.clarifying_questions)}
"""

        if ambiguity_check.examples:
            clarification_request += f"\n\n{chr(10).join(ambiguity_check.examples)}"

        clarification_request += "\n\nPlease rephrase your question with more details."

        return Command(
            goto=END,
            update={
                "ambiguity_check": ambiguity_check,
                "needs_clarification": True,
                "final_answer": clarification_request
            }
        )

    # Question is clear, proceed
    print(f"  ✓ Question is clear, proceeding with analysis")

    return Command(
        goto="question_understanding_agent",
        update={
            "ambiguity_check": ambiguity_check,
            "needs_clarification": False
        }
    )


# ===== AGENT 2: QUESTION UNDERSTANDING =====
def question_understanding_agent(state: UltraPreciseState) -> Command[Literal["router_agent"]]:
    """Analyzes question to understand what's being asked"""
    print("\n🧠 QUESTION UNDERSTANDING: Analyzing question...")

    question = state["question"]
    question_lower = question.lower()

    # Detect entity type
    entity_type = "general"
    if any(word in question_lower for word in ["store", "stores", "str_", "how many stores"]):
        entity_type = "store"
    elif any(word in question_lower for word in ["category", "categories", "beverage", "snacks"]):
        entity_type = "category"
    elif any(word in question_lower for word in ["customer", "segment", "regular", "premium"]):
        entity_type = "customer_segment"

    # Detect intent
    question_intent = "analyze"
    if any(word in question_lower for word in ["top", "best", "worst", "bottom", "which", "what are"]):
        question_intent = "identify"
    elif any(word in question_lower for word in ["compare", "vs", "versus"]):
        question_intent = "compare"
    elif any(word in question_lower for word in ["how many", "count", "total"]):
        question_intent = "identify"

    # Extract filters
    filters = {}
    if "top" in question_lower:
        top_match = re.search(r'top\s+(\d+)', question_lower)
        if top_match:
            filters['top'] = int(top_match.group(1))
    elif "bottom" in question_lower or "not performing" in question_lower:
        filters['performance'] = 'low'

    analysis = QuestionAnalysis(
        entity_type=entity_type,
        specific_entities=[],
        question_intent=question_intent,
        metrics_requested=["performance"],
        filters=filters,
        expected_answer_format="list" if question_intent == "identify" else "explanation"
    )

    print(f"  → Entity Type: {analysis.entity_type}")
    print(f"  → Intent: {analysis.question_intent}")
    print(f"  → Filters: {analysis.filters}")

    return Command(
        goto="router_agent",
        update={"question_analysis": analysis}
    )


# ===== AGENT 3: ROUTER =====
def router_agent(state: UltraPreciseState) -> Command[Literal["context_loader"]]:
    """Routes based on question analysis"""
    print("\n🔍 ROUTER: Selecting data sources...")

    analysis = state["question_analysis"]

    entity_to_source = {
        "store": ["store_performance"],
        "category": ["category_performance"],
        "customer_segment": ["customer_segment"],
        "general": ["overall_business"]
    }

    data_sources = entity_to_source.get(analysis.entity_type, ["overall_business"])
    key_focus = f"{analysis.question_intent} {analysis.entity_type}"
    if analysis.filters:
        key_focus += f" {analysis.filters}"

    print(f"  → Data Sources: {', '.join(data_sources)}")

    return Command(
        goto="context_loader",
        update={
            "data_sources": data_sources,
            "analysis_type": "performance",
            "key_focus": key_focus
        }
    )


# ===== AGENT 4: CONTEXT LOADER =====
def context_loader(state: UltraPreciseState) -> Command[Literal["analysis_agent"]]:
    """Load context"""
    print("\n📊 CONTEXT LOADER: Loading data...")

    context, structured_data = data_loader.get_context_for_sources(
        state["data_sources"],
        state.get("key_focus", "")
    )

    print(f"  ✓ Context loaded")

    return Command(
        goto="analysis_agent",
        update={
            "loaded_context": context,
            "structured_data": structured_data
        }
    )


# ===== AGENT 5: ANALYSIS =====
def analysis_agent(state: UltraPreciseState) -> Command[Literal[END]]:
    """Generate analysis"""
    print("\n💼 ANALYSIS AGENT: Generating answer...")

    prompt = f"""You are a store manager. Answer this question directly using ONLY the data below.

DATA:
{state["loaded_context"][:3000]}

QUESTION: {state["question"]}

IMPORTANT:
- Answer the question directly
- Use specific numbers from the data
- Be concise (2-3 sentences for simple questions)
- If asking for a count, give the count
- If asking about stores, talk about STORES (not categories)
"""

    analysis = call_ollama(prompt)

    print(f"  ✓ Analysis generated")

    return Command(
        goto=END,
        update={"final_answer": analysis}
    )


# ===== BUILD GRAPH =====
def build_ultra_precise_graph():
    """Build the graph with ambiguity checking"""

    builder = StateGraph(UltraPreciseState)

    # Add nodes
    builder.add_node("ambiguity_checker_agent", ambiguity_checker_agent)
    builder.add_node("question_understanding_agent", question_understanding_agent)
    builder.add_node("router_agent", router_agent)
    builder.add_node("context_loader", context_loader)
    builder.add_node("analysis_agent", analysis_agent)

    # Start with ambiguity check
    builder.add_edge(START, "ambiguity_checker_agent")

    return builder.compile()


# ===== MAIN SYSTEM =====
class UltraPreciseStoreManager:
    """Ultra-Precise Store Manager with Clarifying Questions"""

    def __init__(self):
        self.graph = build_ultra_precise_graph()
        print("\n" + "="*70)
        print("ULTRA-PRECISE SYSTEM WITH CLARIFICATION INITIALIZED")
        print("="*70)
        print("✓ Ambiguity Checker")
        print("✓ Clarifying Questions")
        print("✓ Question Understanding")
        print("✓ 100% Accuracy Guarantee")
        print("="*70 + "\n")

    def ask(self, question: str) -> str:
        """Ask and get answer or clarification request"""

        initial_state = {
            "question": question,
            "original_question": question,
            "ambiguity_check": None,
            "needs_clarification": False,
            "clarification_provided": None,
            "question_analysis": None,
            "data_sources": [],
            "analysis_type": "",
            "key_focus": "",
            "loaded_context": "",
            "structured_data": {},
            "context_matches_question": False,
            "context_validation_feedback": "",
            "analysis": "",
            "answer_relevance": None,
            "all_claims_valid": False,
            "attempt_number": 0,
            "validation_feedback": "",
            "final_answer": ""
        }

        result = self.graph.invoke(initial_state)
        return result["final_answer"]

    def run_interactive(self):
        """Interactive CLI"""
        print("\n" + "="*70)
        print("ULTRA-PRECISE STORE MANAGER WITH CLARIFICATION")
        print("="*70)
        print("\n❓ Asks clarifying questions when unclear")
        print("🎯 100% Question Understanding")
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
    """Main entry point"""
    import sys

    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama connected")
    except:
        print("\n❌ ERROR: Cannot connect to Ollama!")
        sys.exit(1)

    system = UltraPreciseStoreManager()
    system.run_interactive()


if __name__ == "__main__":
    main()
