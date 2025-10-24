#!/usr/bin/env python3
"""
SMART SIMPLE ANSWERS System
- Detects descriptive statistic queries → Returns JUST THE NUMBER
- No RCA, no analysis on simple questions
- Asks probing questions when unclear
- Complex analysis ONLY when asked
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

# ===== QUESTION INTENT SCHEMAS =====

class QueryIntent(BaseModel):
    """Understanding what type of answer is needed"""
    intent_type: Literal["descriptive_stat", "comparison", "analysis", "recommendation", "unclear"] = Field(
        description="Type of answer needed"
    )
    stat_type: Optional[str] = Field(
        description="For descriptive_stat: count, sum, avg, max, min, total",
        default=None
    )
    entity: Optional[str] = Field(
        description="What entity: stores, campaigns, categories, customers, etc.",
        default=None
    )
    metric: Optional[str] = Field(
        description="What metric: revenue, transactions, count, etc.",
        default=None
    )
    needs_probing: bool = Field(
        description="Whether we need to ask probing questions",
        default=False
    )
    probing_questions: List[str] = Field(
        description="Questions to ask for clarification",
        default=[]
    )


# ===== STATE =====
class SmartState(TypedDict):
    question: str
    query_intent: Optional[QueryIntent]
    data_sources: list[str]
    loaded_context: str
    structured_data: dict
    final_answer: str


# ===== DATA LOADER =====
class DataLoader:
    def __init__(self):
        self.context_data = {}
        self.load_all_data()

    def load_all_data(self):
        print("\n" + "="*70)
        print("LOADING DATA - SMART SIMPLE ANSWERS")
        print("="*70)

        kpi_files = {
            'store_performance': 'kpi_store_performance.csv',
            'category_performance': 'kpi_category_performance.csv',
            'customer_segment': 'kpi_customer_segment.csv',
            'overall_business': 'kpi_overall_business.csv',
        }

        for key, filename in kpi_files.items():
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                self.context_data[key] = df

        print(f"✓ Loaded {len(self.context_data)} datasets")
        print("="*70 + "\n")

    def get_data(self, source: str) -> pd.DataFrame:
        return self.context_data.get(source)


data_loader = DataLoader()


# ===== OLLAMA =====
def call_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2:1b", "prompt": prompt, "stream": False},
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        return ""
    except:
        return ""


# ===== INTENT DETECTOR =====
class IntentDetector:
    """Detects if question wants just a number or complex analysis"""

    @staticmethod
    def detect(question: str) -> QueryIntent:
        q_lower = question.lower().strip()

        # Pattern 1: DESCRIPTIVE STAT - Just wants a number
        descriptive_patterns = {
            "count": ["how many", "count", "number of", "total number"],
            "sum": ["total", "sum of", "overall"],
            "avg": ["average", "mean"],
            "max": ["highest", "maximum", "most"],
            "min": ["lowest", "minimum", "least"]
        }

        for stat_type, patterns in descriptive_patterns.items():
            if any(pattern in q_lower for pattern in patterns):
                # Detect entity
                entity = None
                if "store" in q_lower:
                    entity = "stores"
                elif "campaign" in q_lower:
                    entity = "campaigns"
                elif "categor" in q_lower:
                    entity = "categories"
                elif "product" in q_lower:
                    entity = "products"
                elif "customer" in q_lower:
                    entity = "customers"

                if entity:
                    return QueryIntent(
                        intent_type="descriptive_stat",
                        stat_type=stat_type,
                        entity=entity,
                        metric="count" if stat_type == "count" else "value",
                        needs_probing=False
                    )

        # Pattern 2: COMPARISON - Wants to compare things
        if any(word in q_lower for word in ["compare", "vs", "versus", "difference between", "gap"]):
            # Check if specific entities mentioned
            has_specifics = bool(re.search(r'STR_\d+', question)) or \
                           any(cat in question for cat in ["Beverages", "Snacks", "Dairy"])

            if has_specifics:
                return QueryIntent(
                    intent_type="comparison",
                    needs_probing=False
                )
            else:
                return QueryIntent(
                    intent_type="unclear",
                    needs_probing=True,
                    probing_questions=[
                        "What would you like to compare?",
                        "Please specify:",
                        "  • Specific stores (e.g., STR_002 vs STR_041)",
                        "  • Categories (e.g., Beverages vs Snacks)",
                        "  • Time periods (e.g., this month vs last month)"
                    ]
                )

        # Pattern 3: ANALYSIS - Wants why/how/insights
        if any(word in q_lower for word in ["why", "how can", "what should", "not performing", "underperform", "poor"]):
            return QueryIntent(
                intent_type="analysis",
                needs_probing=False
            )

        # Pattern 4: RECOMMENDATION - Wants action
        if any(word in q_lower for word in ["recommend", "should", "prioritize", "focus", "improve", "strategy"]):
            return QueryIntent(
                intent_type="recommendation",
                needs_probing=False
            )

        # Pattern 5: UNCLEAR - Too vague
        if len(q_lower.split()) <= 3 or q_lower in ["status", "update", "how", "what"]:
            return QueryIntent(
                intent_type="unclear",
                needs_probing=True,
                probing_questions=[
                    "I need more context to help you.",
                    "What would you like to know?",
                    "  • A specific number? (e.g., 'How many stores?')",
                    "  • Performance analysis? (e.g., 'Which stores are underperforming?')",
                    "  • A recommendation? (e.g., 'Which segment should we prioritize?')"
                ]
            )

        # Default: Try to be helpful but ask for clarity
        return QueryIntent(
            intent_type="unclear",
            needs_probing=True,
            probing_questions=[
                "Could you be more specific?",
                "For example:",
                "  • 'How many stores do we have?'",
                "  • 'What is total revenue?'",
                "  • 'Which categories are performing well?'"
            ]
        )


# ===== AGENT 1: INTENT ANALYZER =====
def intent_analyzer(state: SmartState) -> Command[Literal["probing_agent", "simple_stat_agent", "analysis_agent"]]:
    """Analyze intent and route accordingly"""
    print("\n🧠 INTENT ANALYZER: Understanding what you're asking for...")

    question = state["question"]
    intent = IntentDetector.detect(question)

    print(f"  → Intent Type: {intent.intent_type}")

    if intent.intent_type == "descriptive_stat":
        print(f"  → Stat Type: {intent.stat_type}")
        print(f"  → Entity: {intent.entity}")
        print(f"  → Mode: SIMPLE STAT (just return the number)")

        return Command(
            goto="simple_stat_agent",
            update={"query_intent": intent}
        )

    elif intent.needs_probing:
        print(f"  → Mode: UNCLEAR - asking probing questions")

        return Command(
            goto="probing_agent",
            update={"query_intent": intent}
        )

    else:
        print(f"  → Mode: COMPLEX ANALYSIS needed")

        return Command(
            goto="analysis_agent",
            update={"query_intent": intent}
        )


# ===== AGENT 2: PROBING QUESTIONS =====
def probing_agent(state: SmartState) -> Command[Literal[END]]:
    """Ask probing questions for unclear queries"""
    print("\n❓ PROBING: Asking for clarification...")

    intent = state["query_intent"]

    response = "\n".join(intent.probing_questions)

    return Command(
        goto=END,
        update={"final_answer": response}
    )


# ===== AGENT 3: SIMPLE STAT AGENT =====
def simple_stat_agent(state: SmartState) -> Command[Literal[END]]:
    """Return JUST THE NUMBER for descriptive stat queries"""
    print("\n📊 SIMPLE STAT: Calculating the number...")

    intent = state["query_intent"]
    entity = intent.entity
    stat_type = intent.stat_type

    answer = ""

    # Get the count/stat
    if entity == "stores":
        df = data_loader.get_data('store_performance')
        if df is not None:
            if stat_type == "count":
                count = len(df)
                answer = f"**{count} stores**"
            elif stat_type == "sum" and "revenue" in state["question"].lower():
                total = df['Total_Revenue'].sum() / 1_000_000
                answer = f"**₹{total:.1f}M total revenue**"
            elif stat_type == "avg" and "revenue" in state["question"].lower():
                avg = df['Total_Revenue'].mean() / 1_000_000
                answer = f"**₹{avg:.1f}M average revenue per store**"

    elif entity == "categories":
        df = data_loader.get_data('category_performance')
        if df is not None:
            if stat_type == "count":
                count = len(df)
                answer = f"**{count} categories**"
            elif stat_type == "sum" and "revenue" in state["question"].lower():
                total = df['Total_Revenue'].sum() / 1_000_000
                answer = f"**₹{total:.1f}M total revenue**"

    elif entity == "campaigns":
        # Check if we have campaign data
        answer = f"**Campaign data not available in current dataset**"
        print(f"  ⚠️  No campaign data loaded")

    elif entity == "customers":
        df = data_loader.get_data('customer_segment')
        if df is not None:
            if stat_type == "count":
                total = df['Total_Customers'].sum()
                answer = f"**{total:,} customers**"

    if not answer:
        answer = "Data not available for this query."

    print(f"  ✓ Answer: {answer}")

    return Command(
        goto=END,
        update={"final_answer": answer}
    )


# ===== AGENT 4: ANALYSIS AGENT =====
def analysis_agent(state: SmartState) -> Command[Literal[END]]:
    """Do complex analysis only when actually requested"""
    print("\n💼 ANALYSIS: Generating detailed analysis...")

    intent = state["query_intent"]
    question = state["question"]

    # Load relevant data
    if "store" in question.lower():
        df = data_loader.get_data('store_performance')
        data_source = "store_performance"
    elif "categor" in question.lower():
        df = data_loader.get_data('category_performance')
        data_source = "category_performance"
    elif "customer" in question.lower():
        df = data_loader.get_data('customer_segment')
        data_source = "customer_segment"
    else:
        df = data_loader.get_data('overall_business')
        data_source = "overall_business"

    if df is None:
        return Command(
            goto=END,
            update={"final_answer": "Data not available."}
        )

    # Create context
    context = df.to_string(index=False)[:3000]

    # Generate analysis based on intent
    if intent.intent_type == "analysis":
        prompt = f"""You are a store manager. Analyze this question and provide insights.

DATA:
{context}

QUESTION: {question}

Provide:
1. Direct answer (2-3 sentences)
2. Key insight (1 sentence explaining why)
3. One actionable recommendation

Keep it concise - total 100-150 words max."""

    elif intent.intent_type == "recommendation":
        prompt = f"""You are a store manager. Provide a strategic recommendation.

DATA:
{context}

QUESTION: {question}

Provide:
1. Your recommendation (1-2 sentences)
2. Why (1 sentence with data)
3. Expected impact (1 sentence with numbers)

Keep it concise - total 100 words max."""

    elif intent.intent_type == "comparison":
        prompt = f"""You are a store manager. Compare the entities mentioned.

DATA:
{context}

QUESTION: {question}

Provide:
1. The comparison (specific numbers)
2. Key difference (1 sentence)
3. What it means (1 sentence)

Keep it concise - total 100 words max."""

    else:
        prompt = f"""Answer this question directly using the data:

DATA:
{context}

QUESTION: {question}

Answer in 2-3 sentences maximum."""

    analysis = call_ollama(prompt)

    print(f"  ✓ Analysis generated")

    return Command(
        goto=END,
        update={"final_answer": analysis}
    )


# ===== BUILD GRAPH =====
def build_smart_graph():
    builder = StateGraph(SmartState)

    builder.add_node("intent_analyzer", intent_analyzer)
    builder.add_node("probing_agent", probing_agent)
    builder.add_node("simple_stat_agent", simple_stat_agent)
    builder.add_node("analysis_agent", analysis_agent)

    builder.add_edge(START, "intent_analyzer")

    return builder.compile()


# ===== MAIN SYSTEM =====
class SmartStoreManager:
    """Smart Store Manager - Simple questions get simple answers"""

    def __init__(self):
        self.graph = build_smart_graph()
        print("\n" + "="*70)
        print("SMART STORE MANAGER INITIALIZED")
        print("="*70)
        print("✓ Descriptive Stats → Just the number")
        print("✓ Complex Analysis → Only when asked")
        print("✓ Unclear → Probing questions")
        print("="*70 + "\n")

    def ask(self, question: str) -> str:
        initial_state = {
            "question": question,
            "query_intent": None,
            "data_sources": [],
            "loaded_context": "",
            "structured_data": {},
            "final_answer": ""
        }

        result = self.graph.invoke(initial_state)
        return result["final_answer"]

    def run_interactive(self):
        print("\n" + "="*70)
        print("SMART STORE MANAGER")
        print("="*70)
        print("\n💡 Examples:")
        print("  Simple: 'How many stores?' → Just the number")
        print("  Complex: 'Why are stores underperforming?' → Full analysis")
        print("  Unclear: 'Status' → Probing questions")
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

    system = SmartStoreManager()
    system.run_interactive()


if __name__ == "__main__":
    main()
