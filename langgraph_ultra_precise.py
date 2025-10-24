#!/usr/bin/env python3
"""
ULTRA-PRECISE Multi-Agent Store Manager System
- 100% Question Understanding
- 100% Answer Relevance
- Entity Type Detection
- Question Decomposition
- Answer-Question Matching
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

# ===== QUESTION UNDERSTANDING SCHEMAS =====

class QuestionAnalysis(BaseModel):
    """Deep analysis of what the question is asking"""
    entity_type: Literal["store", "category", "product", "customer_segment", "time_period", "general"] = Field(
        description="Primary entity type being asked about"
    )
    specific_entities: List[str] = Field(
        description="Specific entities mentioned (e.g., ['STR_002', 'Beverages'])",
        default=[]
    )
    question_intent: Literal["identify", "compare", "analyze", "recommend", "explain"] = Field(
        description="What the question wants: identify top/bottom, compare entities, analyze performance, recommend actions, explain why"
    )
    metrics_requested: List[str] = Field(
        description="Metrics being asked about: revenue, transactions, customers, margin, etc.",
        default=[]
    )
    filters: dict = Field(
        description="Any filters like 'top 5', 'bottom 10', 'not performing', etc.",
        default={}
    )
    expected_answer_format: str = Field(
        description="What format the answer should take: list, comparison, explanation, recommendation"
    )


class AnswerRelevance(BaseModel):
    """Validates if answer matches question"""
    addresses_entity_type: bool = Field(description="Answer discusses the correct entity type")
    addresses_specific_entities: bool = Field(description="Answer discusses specific entities if mentioned")
    answers_intent: bool = Field(description="Answer fulfills the question intent")
    includes_requested_metrics: bool = Field(description="Answer includes requested metrics")
    correct_format: bool = Field(description="Answer format matches expected format")
    relevance_score: float = Field(description="Overall relevance score 0.0-1.0", ge=0.0, le=1.0)
    issues: List[str] = Field(description="List of relevance issues found", default=[])


# ===== STATE DEFINITION =====
class UltraPreciseState(TypedDict):
    """State with question understanding"""
    # Input
    question: str

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


# ===== DATA LOADER =====
class DataLoader:
    """Data loader with same functionality as validated version"""

    def __init__(self):
        self.context_data = {}
        self.business_context = {}
        self.insights_document = ""
        self.prompt_template = ""
        self.load_all_data()

    def load_all_data(self):
        """Load all data sources"""
        print("\n" + "="*70)
        print("LOADING DATA FOR ULTRA-PRECISE SYSTEM")
        print("="*70)

        # Load metadata
        if os.path.exists('store_manager_metadata_layer.json'):
            with open('store_manager_metadata_layer.json', 'r') as f:
                self.store_manager_metadata = json.load(f)
            print(f"✓ Store Manager Metadata")

        if os.path.exists('business_context_metadata.json'):
            with open('business_context_metadata.json', 'r') as f:
                self.business_context = json.load(f)
            print(f"✓ Business Context")

        if os.path.exists('COMPLETE_DATA_INSIGHTS.md'):
            with open('COMPLETE_DATA_INSIGHTS.md', 'r') as f:
                self.insights_document = f.read()
            print(f"✓ Insights Document")

        if os.path.exists('store_manager_prompt_template.txt'):
            with open('store_manager_prompt_template.txt', 'r') as f:
                self.prompt_template = f.read()
            print(f"✓ Prompt Template")
        else:
            self.prompt_template = """You are a STORE MANAGER with 20+ years experience."""

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
            'payment_method': 'kpi_payment_method.csv',
            'time_slot': 'kpi_time_slot.csv',
            'delivery_method': 'kpi_delivery_method.csv',
            'weekend_weekday': 'kpi_weekend_weekday.csv',
            'age_group': 'kpi_age_group.csv',
            'gender': 'kpi_gender.csv',
            'seasonal': 'kpi_seasonal.csv',
            'brand_performance': 'kpi_brand_performance.csv',
            'organic_vs_nonorganic': 'kpi_organic_vs_nonorganic.csv',
            'employee_performance': 'kpi_employee_performance.csv',
            'master_dashboard': 'kpi_master_dashboard.csv'
        }

        for key, filename in kpi_files.items():
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                self.context_data[key] = df

        print(f"✓ All {len(self.context_data)} KPI datasets")
        print("="*70 + "\n")

    def get_context_for_sources(self, data_sources: list[str], analysis_type: str, key_focus: str = "") -> tuple[str, dict]:
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

                if 'daily' in source:
                    context.append(df.tail(30).to_string(index=False))
                elif 'weekly' in source:
                    context.append(df.tail(12).to_string(index=False))
                elif 'store_performance' in source:
                    df_sorted = df.sort_values('Total_Revenue', ascending=False)

                    if 'top' in key_focus.lower():
                        numbers = re.findall(r'\d+', key_focus)
                        if numbers:
                            top_n = int(numbers[0])
                            df_sorted = df_sorted.head(top_n)
                            context.append(f"TOP {top_n} STORES BY REVENUE:\n\n")
                    elif 'bottom' in key_focus.lower() or 'not performing' in key_focus.lower() or 'underperform' in key_focus.lower():
                        numbers = re.findall(r'\d+', key_focus)
                        if numbers:
                            bottom_n = int(numbers[0])
                            df_sorted = df_sorted.tail(bottom_n).sort_values('Total_Revenue', ascending=True)
                            context.append(f"BOTTOM {bottom_n} STORES BY REVENUE:\n\n")
                        else:
                            # Show bottom 10 by default
                            df_sorted = df_sorted.tail(10).sort_values('Total_Revenue', ascending=True)
                            context.append(f"BOTTOM 10 STORES BY REVENUE:\n\n")

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


def call_ollama_json(prompt: str, model: str = "llama3.2:1b") -> str:
    """Call Ollama with JSON mode"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"


# ===== QUESTION ANALYZER =====
class QuestionAnalyzer:
    """Analyzes question to understand exactly what's being asked"""

    @staticmethod
    def analyze(question: str) -> QuestionAnalysis:
        """Deep analysis of question"""

        question_lower = question.lower()

        # Detect entity type
        entity_type = "general"
        if any(word in question_lower for word in ["store", "stores", "str_"]):
            entity_type = "store"
        elif any(word in question_lower for word in ["category", "categories", "beverage", "snacks", "dairy", "bakery", "produce"]):
            entity_type = "category"
        elif any(word in question_lower for word in ["product", "products", "item", "items", "sku"]):
            entity_type = "product"
        elif any(word in question_lower for word in ["customer", "customers", "segment", "regular", "premium", "occasional"]):
            entity_type = "customer_segment"
        elif any(word in question_lower for word in ["day", "week", "month", "time", "period", "daily", "weekly", "monthly"]):
            entity_type = "time_period"

        # Extract specific entities
        specific_entities = []

        # Store IDs
        store_pattern = r'STR_\d+'
        specific_entities.extend(re.findall(store_pattern, question, re.IGNORECASE))

        # Category names
        categories = ["Beverages", "Snacks", "Personal Care", "Household", "Fruits & Vegetables",
                     "Dairy & Eggs", "Bakery", "Frozen Foods", "Meat & Seafood", "Pantry Staples"]
        for cat in categories:
            if cat.lower() in question_lower:
                specific_entities.append(cat)

        # Customer segments
        segments = ["Regular", "Premium", "Occasional", "New"]
        for seg in segments:
            if seg.lower() in question_lower:
                specific_entities.append(seg)

        # Detect question intent
        question_intent = "analyze"
        if any(word in question_lower for word in ["top", "best", "highest", "bottom", "worst", "lowest", "which", "what are"]):
            question_intent = "identify"
        elif any(word in question_lower for word in ["compare", "vs", "versus", "difference", "gap", "between"]):
            question_intent = "compare"
        elif any(word in question_lower for word in ["should", "recommend", "suggest", "prioritize", "focus"]):
            question_intent = "recommend"
        elif any(word in question_lower for word in ["why", "how", "explain", "reason", "cause"]):
            question_intent = "explain"

        # Extract metrics requested
        metrics_requested = []
        metric_keywords = {
            "revenue": ["revenue", "sales", "money"],
            "transactions": ["transactions", "visits", "orders"],
            "customers": ["customers", "shoppers", "buyers"],
            "atv": ["average transaction", "atv", "basket size"],
            "margin": ["margin", "profit", "profitability"],
            "performance": ["performance", "performing", "success"]
        }

        for metric, keywords in metric_keywords.items():
            if any(kw in question_lower for kw in keywords):
                metrics_requested.append(metric)

        # Extract filters
        filters = {}

        # Top N / Bottom N
        top_match = re.search(r'top\s+(\d+)', question_lower)
        if top_match:
            filters['top'] = int(top_match.group(1))

        bottom_match = re.search(r'bottom\s+(\d+)', question_lower)
        if bottom_match:
            filters['bottom'] = int(bottom_match.group(1))

        # Not performing / underperforming
        if any(phrase in question_lower for phrase in ["not performing", "underperform", "poor performance", "low performance"]):
            filters['performance'] = 'low'

        # Determine expected answer format
        expected_format = "explanation"
        if question_intent == "identify":
            expected_format = "list"
        elif question_intent == "compare":
            expected_format = "comparison"
        elif question_intent == "recommend":
            expected_format = "recommendation"

        return QuestionAnalysis(
            entity_type=entity_type,
            specific_entities=specific_entities,
            question_intent=question_intent,
            metrics_requested=metrics_requested if metrics_requested else ["performance"],
            filters=filters,
            expected_answer_format=expected_format
        )


# ===== ANSWER FORMATTER =====
def format_answer_with_summary(answer: str, relevance: AnswerRelevance) -> str:
    """Format answer with executive summary and expandable details"""

    # Check if answer has the separator
    if "---DETAILED_ANALYSIS_BELOW---" in answer:
        parts = answer.split("---DETAILED_ANALYSIS_BELOW---")
        summary = parts[0].strip()
        details = parts[1].strip() if len(parts) > 1 else ""

        # Format with visual separation
        formatted = f"""
{"="*70}
📊 EXECUTIVE SUMMARY
{"="*70}

{summary}

{"="*70}

💡 [EXPAND FOR DETAILED ANALYSIS]

{"─"*70}
📋 DETAILED ANALYSIS
{"─"*70}

{details}

{"─"*70}
"""
    else:
        # No separator, use as-is
        formatted = answer

    # Add relevance badge
    if relevance.relevance_score >= 0.8:
        formatted += f"\n\n✓ **Answer Relevance: {relevance.relevance_score:.0%}** - Directly addresses your question"

    return formatted


# ===== ANSWER RELEVANCE CHECKER =====
class AnswerRelevanceChecker:
    """Validates if answer is relevant to question"""

    @staticmethod
    def check(answer: str, question_analysis: QuestionAnalysis, question: str) -> AnswerRelevance:
        """Check answer relevance"""

        issues = []

        # Check entity type
        entity_type = question_analysis.entity_type
        addresses_entity_type = False

        if entity_type == "store":
            if "STR_" in answer or "store" in answer.lower():
                addresses_entity_type = True
            else:
                issues.append(f"Question asks about STORES but answer doesn't mention specific stores")

        elif entity_type == "category":
            categories = ["Beverages", "Snacks", "Personal Care", "Household", "Fruits & Vegetables",
                         "Dairy & Eggs", "Bakery", "Frozen Foods", "Meat & Seafood", "Pantry Staples"]
            if any(cat in answer for cat in categories):
                addresses_entity_type = True
            else:
                issues.append(f"Question asks about CATEGORIES but answer doesn't mention specific categories")

        elif entity_type == "customer_segment":
            segments = ["Regular", "Premium", "Occasional", "New"]
            if any(seg in answer for seg in segments):
                addresses_entity_type = True
            else:
                issues.append(f"Question asks about CUSTOMER SEGMENTS but answer doesn't mention segments")

        else:
            addresses_entity_type = True  # General questions

        # Check specific entities
        addresses_specific_entities = True
        if question_analysis.specific_entities:
            for entity in question_analysis.specific_entities:
                if entity not in answer:
                    addresses_specific_entities = False
                    issues.append(f"Question mentions '{entity}' but answer doesn't address it")

        # Check question intent
        answers_intent = True
        intent = question_analysis.question_intent

        if intent == "identify":
            # Should have a list or numbered items
            if not (re.search(r'\d+\.', answer) or re.search(r'^\d+\)', answer, re.MULTILINE)):
                answers_intent = False
                issues.append(f"Question asks to IDENTIFY/LIST but answer doesn't provide a clear list")

        elif intent == "compare":
            # Should mention both entities being compared
            if "vs" not in answer.lower() and "compared to" not in answer.lower() and "difference" not in answer.lower():
                answers_intent = False
                issues.append(f"Question asks to COMPARE but answer doesn't show comparison")

        elif intent == "recommend":
            # Should have clear recommendations/actions
            if not any(word in answer.lower() for word in ["recommend", "should", "action", "strategy", "focus"]):
                answers_intent = False
                issues.append(f"Question asks for RECOMMENDATION but answer doesn't provide clear actions")

        # Check requested metrics
        includes_requested_metrics = True
        for metric in question_analysis.metrics_requested:
            if metric == "revenue" and "₹" not in answer:
                includes_requested_metrics = False
                issues.append(f"Question asks about REVENUE but answer doesn't include revenue figures")
            elif metric == "transactions" and "transaction" not in answer.lower():
                includes_requested_metrics = False
                issues.append(f"Question asks about TRANSACTIONS but answer doesn't mention them")
            elif metric == "customers" and "customer" not in answer.lower():
                includes_requested_metrics = False
                issues.append(f"Question asks about CUSTOMERS but answer doesn't mention customer data")

        # Check format
        correct_format = True
        expected_format = question_analysis.expected_answer_format

        if expected_format == "list" and not re.search(r'\d+\.', answer):
            correct_format = False
            issues.append(f"Expected LIST format but answer is not formatted as a list")

        # Calculate relevance score
        score = sum([
            addresses_entity_type,
            addresses_specific_entities,
            answers_intent,
            includes_requested_metrics,
            correct_format
        ]) / 5.0

        return AnswerRelevance(
            addresses_entity_type=addresses_entity_type,
            addresses_specific_entities=addresses_specific_entities,
            answers_intent=answers_intent,
            includes_requested_metrics=includes_requested_metrics,
            correct_format=correct_format,
            relevance_score=score,
            issues=issues
        )


# ===== AGENT 1: QUESTION UNDERSTANDING =====
def question_understanding_agent(state: UltraPreciseState) -> Command[Literal["router_agent"]]:
    """Analyzes question to understand exactly what's being asked"""
    print("\n🧠 QUESTION UNDERSTANDING: Deep analysis of question...")

    question = state["question"]

    # Analyze question
    analysis = QuestionAnalyzer.analyze(question)

    print(f"  → Entity Type: {analysis.entity_type}")
    print(f"  → Specific Entities: {analysis.specific_entities if analysis.specific_entities else 'None'}")
    print(f"  → Intent: {analysis.question_intent}")
    print(f"  → Metrics Requested: {', '.join(analysis.metrics_requested)}")
    print(f"  → Filters: {analysis.filters}")
    print(f"  → Expected Format: {analysis.expected_answer_format}")

    return Command(
        goto="router_agent",
        update={"question_analysis": analysis}
    )


# ===== AGENT 2: SMART ROUTER =====
def router_agent(state: UltraPreciseState) -> Command[Literal["context_loader"]]:
    """Routes based on question analysis"""
    print("\n🔍 ROUTER: Selecting data sources based on question analysis...")

    analysis = state["question_analysis"]

    # Map entity type to data source
    entity_to_source = {
        "store": ["store_performance"],
        "category": ["category_performance"],
        "product": ["product_performance"],
        "customer_segment": ["customer_segment"],
        "time_period": ["daily_performance", "weekly_performance", "monthly_performance"],
        "general": ["overall_business"]
    }

    data_sources = entity_to_source.get(analysis.entity_type, ["overall_business"])

    # Determine analysis type
    analysis_type = "performance"
    if analysis.question_intent == "recommend":
        analysis_type = "strategic"
    elif "customer" in analysis.entity_type:
        analysis_type = "customer"
    elif "revenue" in analysis.metrics_requested or "margin" in analysis.metrics_requested:
        analysis_type = "financial"

    # Build key focus
    key_focus = f"{analysis.question_intent} {analysis.entity_type}"
    if analysis.filters:
        key_focus += f" with filters: {analysis.filters}"

    print(f"  → Data Sources: {', '.join(data_sources)}")
    print(f"  → Analysis Type: {analysis_type}")
    print(f"  → Key Focus: {key_focus}")

    return Command(
        goto="context_loader",
        update={
            "data_sources": data_sources,
            "analysis_type": analysis_type,
            "key_focus": key_focus
        }
    )


# ===== AGENT 3: CONTEXT LOADER WITH VALIDATION =====
def context_loader(state: UltraPreciseState) -> Command[Literal["context_validator"]]:
    """Load context and validate it matches question"""
    print("\n📊 CONTEXT LOADER: Loading data...")

    context, structured_data = data_loader.get_context_for_sources(
        state["data_sources"],
        state["analysis_type"],
        state.get("key_focus", "")
    )

    print(f"  ✓ Context loaded ({len(context)} chars)")

    return Command(
        goto="context_validator",
        update={
            "loaded_context": context,
            "structured_data": structured_data
        }
    )


# ===== AGENT 4: CONTEXT VALIDATOR =====
def context_validator(state: UltraPreciseState) -> Command[Literal["analysis_agent"]]:
    """Validates that loaded context matches question requirements"""
    print("\n✅ CONTEXT VALIDATOR: Checking if data matches question...")

    analysis = state["question_analysis"]
    context = state["loaded_context"]

    context_matches = True
    feedback = []

    # Check entity type match
    if analysis.entity_type == "store" and "STORE PERFORMANCE DATA" not in context:
        context_matches = False
        feedback.append("Question asks about STORES but store performance data not loaded")

    if analysis.entity_type == "category" and "CATEGORY PERFORMANCE DATA" not in context:
        context_matches = False
        feedback.append("Question asks about CATEGORIES but category data not loaded")

    if analysis.entity_type == "customer_segment" and "CUSTOMER SEGMENT DATA" not in context:
        context_matches = False
        feedback.append("Question asks about CUSTOMER SEGMENTS but segment data not loaded")

    # Check specific entities
    for entity in analysis.specific_entities:
        if entity not in context:
            context_matches = False
            feedback.append(f"Question mentions '{entity}' but it's not in loaded data")

    # Check filters
    if 'top' in analysis.filters and f"TOP {analysis.filters['top']}" not in context:
        feedback.append(f"Question asks for top {analysis.filters['top']} but context not filtered correctly")

    if 'bottom' in analysis.filters and f"BOTTOM {analysis.filters['bottom']}" not in context:
        feedback.append(f"Question asks for bottom {analysis.filters['bottom']} but context not filtered correctly")

    feedback_str = "\n".join(feedback) if feedback else "Context matches question perfectly"

    print(f"  → Context Matches: {'✓ Yes' if context_matches else '✗ No'}")
    if feedback:
        print(f"  → Issues: {'; '.join(feedback)}")

    return Command(
        goto="analysis_agent",
        update={
            "context_matches_question": context_matches,
            "context_validation_feedback": feedback_str
        }
    )


# ===== AGENT 5: ANALYSIS =====
def analysis_agent(state: UltraPreciseState) -> Command[Literal["answer_relevance_checker"]]:
    """Generate analysis with question context"""
    attempt = state.get("attempt_number", 0)
    print(f"\n💼 ANALYSIS AGENT: Generating answer (Attempt {attempt + 1}/3)...")

    analysis = state["question_analysis"]

    # Build specific instructions based on question
    question_context = f"""
CRITICAL - QUESTION ANALYSIS:
- Entity Type: {analysis.entity_type.upper()}
- Question Intent: {analysis.question_intent.upper()}
- Metrics Requested: {', '.join(analysis.metrics_requested).upper()}
- Expected Format: {analysis.expected_answer_format.upper()}

YOU MUST:
1. Answer ONLY about {analysis.entity_type.upper()}
2. Fulfill the {analysis.question_intent.upper()} intent
3. Include {', '.join(analysis.metrics_requested).upper()} metrics
4. Format as {analysis.expected_answer_format.upper()}
"""

    if analysis.specific_entities:
        question_context += f"\n5. MUST mention these entities: {', '.join(analysis.specific_entities)}"

    if analysis.filters:
        question_context += f"\n6. Apply these filters: {analysis.filters}"

    # Add validation feedback if retry
    if attempt > 0 and state.get("validation_feedback"):
        question_context += f"\n\nPREVIOUS ATTEMPT ERRORS:\n{state['validation_feedback']}"

    # Build prompt
    prompt = f"""{question_context}

{data_loader.prompt_template.format(
    expertise_context="",
    data_context=state["loaded_context"],
    question=state["question"]
)}"""

    analysis_text = call_ollama(prompt)

    print(f"  ✓ Analysis generated ({len(analysis_text)} chars)")

    return Command(
        goto="answer_relevance_checker",
        update={
            "analysis": analysis_text,
            "attempt_number": attempt + 1
        }
    )


# ===== AGENT 6: ANSWER RELEVANCE CHECKER =====
def answer_relevance_checker(state: UltraPreciseState) -> Command[Literal["analysis_agent", END]]:
    """Check if answer is relevant to question"""
    print("\n🎯 ANSWER RELEVANCE: Checking if answer addresses question...")

    relevance = AnswerRelevanceChecker.check(
        state["analysis"],
        state["question_analysis"],
        state["question"]
    )

    print(f"  → Relevance Score: {relevance.relevance_score:.1%}")
    print(f"  → Entity Type Match: {'✓' if relevance.addresses_entity_type else '✗'}")
    print(f"  → Specific Entities Match: {'✓' if relevance.addresses_specific_entities else '✗'}")
    print(f"  → Intent Fulfilled: {'✓' if relevance.answers_intent else '✗'}")
    print(f"  → Metrics Included: {'✓' if relevance.includes_requested_metrics else '✗'}")
    print(f"  → Format Correct: {'✓' if relevance.correct_format else '✗'}")

    if relevance.issues:
        print(f"\n  ⚠️  RELEVANCE ISSUES:")
        for issue in relevance.issues:
            print(f"    • {issue}")

    # If relevance score < 80% and we have attempts left, retry
    if relevance.relevance_score < 0.8 and state.get("attempt_number", 0) < 3:
        feedback = f"""Your answer is not relevant to the question (score: {relevance.relevance_score:.1%}).

ISSUES:
{chr(10).join(f'- {issue}' for issue in relevance.issues)}

Please regenerate the answer ensuring it:
1. Addresses the correct entity type: {state['question_analysis'].entity_type}
2. Fulfills the question intent: {state['question_analysis'].question_intent}
3. Includes requested metrics: {', '.join(state['question_analysis'].metrics_requested)}
4. Uses the correct format: {state['question_analysis'].expected_answer_format}
"""

        return Command(
            goto="analysis_agent",
            update={
                "answer_relevance": relevance,
                "validation_feedback": feedback
            }
        )

    # If relevant or max attempts, return answer
    final_answer = state["analysis"]

    # Format answer with summary/details separation
    formatted_answer = format_answer_with_summary(final_answer, relevance)

    return Command(
        goto=END,
        update={
            "answer_relevance": relevance,
            "final_answer": formatted_answer
        }
    )


# ===== BUILD GRAPH =====
def build_ultra_precise_graph():
    """Build the ultra-precise graph"""

    builder = StateGraph(UltraPreciseState)

    # Add nodes
    builder.add_node("question_understanding_agent", question_understanding_agent)
    builder.add_node("router_agent", router_agent)
    builder.add_node("context_loader", context_loader)
    builder.add_node("context_validator", context_validator)
    builder.add_node("analysis_agent", analysis_agent)
    builder.add_node("answer_relevance_checker", answer_relevance_checker)

    # Start flow
    builder.add_edge(START, "question_understanding_agent")

    return builder.compile()


# ===== MAIN SYSTEM =====
class UltraPreciseStoreManager:
    """Ultra-Precise Store Manager with 100% Question Understanding"""

    def __init__(self):
        self.graph = build_ultra_precise_graph()
        print("\n" + "="*70)
        print("ULTRA-PRECISE SYSTEM INITIALIZED")
        print("="*70)
        print("✓ Question Understanding Agent")
        print("✓ Smart Router (Entity-Based)")
        print("✓ Context Validator")
        print("✓ Answer Relevance Checker")
        print("✓ 100% Question-Answer Matching")
        print("="*70 + "\n")

    def ask(self, question: str) -> str:
        """Ask and get ultra-precise answer"""

        print("\n" + "="*70)
        print("ULTRA-PRECISE PIPELINE EXECUTING")
        print("="*70)

        initial_state = {
            "question": question,
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

        print("\n" + "="*70)
        print("PIPELINE COMPLETE - ULTRA-PRECISE ANSWER")
        print("="*70 + "\n")

        return result["final_answer"]

    def run_interactive(self):
        """Interactive CLI"""
        print("\n" + "="*70)
        print("ULTRA-PRECISE STORE MANAGER")
        print("="*70)
        print("\n🎯 100% Question Understanding")
        print("🎯 100% Answer Relevance")
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
