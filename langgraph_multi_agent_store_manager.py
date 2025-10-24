#!/usr/bin/env python3
"""
TRUE Multi-Agent Store Manager System using LangGraph
- Proper agent separation with StateGraph
- Agent-to-agent communication via Command
- State management across agents
- Conditional routing
"""

import pandas as pd
import json
import os
import re
from typing import Annotated, Literal, TypedDict
from typing_extensions import TypedDict as TypedDictExt
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
import requests

# ===== STATE DEFINITION =====
class StoreManagerState(TypedDict):
    """Shared state across all agents"""
    # Input
    question: str

    # Router outputs
    data_sources: list[str]
    analysis_type: str
    key_focus: str

    # Context data
    loaded_context: str

    # Analysis outputs
    analysis: str
    facts_verified: bool

    # Verification outputs
    extracted_claims: list[str]
    verified_analysis: str

    # Final output
    final_answer: str


# ===== DATA LOADER =====
class DataLoader:
    """Centralized data loading with caching"""

    def __init__(self):
        self.context_data = {}
        self.business_context = {}
        self.insights_document = ""
        self.prompt_template = ""
        self.load_all_data()

    def load_all_data(self):
        """Load all data sources once"""
        print("\n" + "="*70)
        print("LOADING DATA FOR LANGGRAPH MULTI-AGENT SYSTEM")
        print("="*70)

        # Store Manager Metadata Layer (NEW - Comprehensive)
        self.store_manager_metadata = {}
        if os.path.exists('store_manager_metadata_layer.json'):
            with open('store_manager_metadata_layer.json', 'r') as f:
                self.store_manager_metadata = json.load(f)
            print(f"✓ Store Manager Metadata Layer (comprehensive)")

        # Business context metadata
        if os.path.exists('business_context_metadata.json'):
            with open('business_context_metadata.json', 'r') as f:
                self.business_context = json.load(f)
            print(f"✓ Business intelligence metadata")

        # Insights document
        if os.path.exists('COMPLETE_DATA_INSIGHTS.md'):
            with open('COMPLETE_DATA_INSIGHTS.md', 'r') as f:
                self.insights_document = f.read()
            print(f"✓ Strategic insights document")

        # Prompt template (customizable)
        if os.path.exists('store_manager_prompt_template.txt'):
            with open('store_manager_prompt_template.txt', 'r') as f:
                self.prompt_template = f.read()
            print(f"✓ Store Manager prompt template (customizable)")
        else:
            # Fallback to default prompt if file doesn't exist
            self.prompt_template = """You are a STORE MANAGER with 20+ years experience.
Analyze the data provided and give brief, actionable insights."""

        # KPI dashboard
        if os.path.exists('store_manager_kpi_dashboard.csv'):
            df = pd.read_csv('store_manager_kpi_dashboard.csv')
            self.context_data['comprehensive_kpis'] = df
            print(f"✓ Master KPI dashboard ({len(df)} metrics)")

        # All KPI files
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

    def get_context_for_sources(self, data_sources: list[str], analysis_type: str, key_focus: str = "") -> str:
        """Load specific context based on routing decision"""
        context = []

        # Ensure data_sources is a list
        if isinstance(data_sources, str):
            data_sources = [data_sources]

        # Load requested CSV data
        for source in data_sources:
            if source in self.context_data:
                df = self.context_data[source]
                context.append(f"\n=== {source.upper().replace('_', ' ')} DATA ===\n")

                # Load appropriate amount of data
                if 'daily' in source:
                    context.append(df.tail(30).to_string(index=False))
                elif 'weekly' in source:
                    context.append(df.tail(12).to_string(index=False))
                elif 'store_performance' in source:
                    # For store performance, show stores sorted by revenue
                    df_sorted = df.sort_values('Total_Revenue', ascending=False)

                    # If asking for "top X", show only those X stores
                    if 'top' in key_focus.lower():
                        # Extract number (top 5, top 10, etc.)
                        import re
                        numbers = re.findall(r'\d+', key_focus)
                        if numbers:
                            top_n = int(numbers[0])
                            df_sorted = df_sorted.head(top_n)
                            context.append(f"TOP {top_n} STORES BY REVENUE (Sorted Highest to Lowest):\n\n")

                    context.append(df_sorted.to_string(index=False))
                elif len(df) > 50:
                    context.append(df.head(50).to_string(index=False))
                else:
                    context.append(df.to_string(index=False))
                context.append("\n\n")
            else:
                print(f"  ⚠️  Warning: '{source}' not found in loaded data")

        # Add business intelligence based on analysis type
        if analysis_type in ['strategic', 'financial'] and 'financial_opportunities' in self.business_context:
            fo = self.business_context['financial_opportunities']
            context.append("\n=== FINANCIAL OPPORTUNITIES ===\n")
            context.append(f"Total Potential: {fo.get('total_potential', 'N/A')}\n")
            for init in fo.get('breakdown', [])[:5]:
                context.append(f"  • {init.get('initiative')}: {init.get('impact')} (ROI: {init.get('roi')})\n")
            context.append("\n")

        if analysis_type == 'customer' and 'customer_intelligence' in self.business_context:
            ci = self.business_context['customer_intelligence']
            context.append("\n=== CUSTOMER INTELLIGENCE ===\n")
            for segment in ['Regular', 'Premium', 'Occasional', 'New']:
                if segment in ci:
                    seg = ci[segment]
                    context.append(f"\n{segment}: {seg.get('count', 'N/A')}\n")
                    context.append(f"  Strategy: {seg.get('strategy', 'N/A')}\n")
            context.append("\n")

        return "".join(context)


# Global data loader instance
data_loader = DataLoader()

# Ollama client
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


# ===== AGENT 1: ROUTER =====
def router_agent(state: StoreManagerState) -> Command[Literal["context_loader"]]:
    """
    ROUTER AGENT - Analyzes query and determines what's needed
    """
    print("\n🔍 ROUTER AGENT: Analyzing query...")

    question = state["question"]

    router_prompt = f"""You are a Query Router for a grocery retail business intelligence system.

Analyze this question and determine what data is needed.

Available Data Sources:
- overall_business, store_performance, category_performance, product_performance
- customer_segment, daily_performance, weekly_performance, monthly_performance
- payment_method, time_slot, delivery_method, weekend_weekday
- age_group, gender, seasonal, brand_performance, organic_vs_nonorganic, employee_performance

Analysis Types: strategic, operational, financial, customer, product, performance

Question: "{question}"

ROUTING RULES:
- If asking about "stores" or "top stores" → use ONLY ["store_performance"]
- If asking about "categories" → use ONLY ["category_performance"]
- If asking about "products" → use ONLY ["product_performance"]
- If asking about "customers" or "segments" → use ONLY ["customer_segment"]
- Only select multiple sources if the question explicitly needs them

Respond with ONLY this JSON (no other text):
{{
    "data_sources": ["source1", "source2"],
    "analysis_type": "type",
    "key_focus": "brief focus description"
}}

Example:
Question: "Which are the top 5 stores?"
Response: {{"data_sources": ["store_performance"], "analysis_type": "performance", "key_focus": "top performing stores"}}"""

    response = call_ollama(router_prompt)

    # Parse routing decision
    try:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            routing = json.loads(json_match.group())
        else:
            routing = {
                "data_sources": ["overall_business", "comprehensive_kpis"],
                "analysis_type": "strategic",
                "key_focus": "general analysis"
            }
    except:
        routing = {
            "data_sources": ["overall_business"],
            "analysis_type": "strategic",
            "key_focus": "general analysis"
        }

    print(f"  → Type: {routing['analysis_type']}")
    print(f"  → Sources: {', '.join(routing['data_sources'][:5])}")
    print(f"  → Focus: {routing['key_focus']}")

    # Update state and route to context loader
    return Command(
        goto="context_loader",
        update={
            "data_sources": routing["data_sources"],
            "analysis_type": routing["analysis_type"],
            "key_focus": routing["key_focus"]
        }
    )


# ===== CONTEXT LOADER (Helper Node) =====
def context_loader(state: StoreManagerState) -> Command[Literal["analysis_agent"]]:
    """
    CONTEXT LOADER - Loads relevant data based on routing
    """
    print("\n📊 CONTEXT LOADER: Loading relevant data...")

    context = data_loader.get_context_for_sources(
        state["data_sources"],
        state["analysis_type"],
        state.get("key_focus", "")
    )

    print(f"  ✓ Context prepared ({len(context)} chars)")

    return Command(
        goto="analysis_agent",
        update={"loaded_context": context}
    )


# ===== AGENT 2: ANALYSIS (WITH COMPREHENSIVE METADATA) =====
def analysis_agent(state: StoreManagerState) -> Command[Literal["verification_agent"]]:
    """
    ANALYSIS AGENT - Generates insights with deep retail expertise
    """
    print("\n💼 ANALYSIS AGENT: Generating strategic insights with store manager expertise...")

    # Get metadata for enhanced context
    metadata = data_loader.store_manager_metadata

    # Build comprehensive domain expertise context
    expertise_context = ""
    if metadata:
        # Add persona and expertise
        persona = metadata.get('persona', {})
        expertise_context += f"\n=== YOUR EXPERTISE ===\n"
        expertise_context += f"Role: {persona.get('role', 'Store Manager')}\n"
        expertise_context += f"Experience: {persona.get('experience_level', '20+ years')}\n"
        expertise_context += f"Communication Style: {persona.get('communication_style', 'Data-driven, actionable')}\n"

        # Add business overview
        business = metadata.get('business_overview', {})
        expertise_context += f"\n=== BUSINESS CONTEXT ===\n"
        expertise_context += f"Company: {business.get('company_type', 'Multi-store Grocery Retail')}\n"
        expertise_context += f"Stores: {business.get('total_stores', 50)} locations\n"
        expertise_context += f"Regions: {', '.join(business.get('geographic_coverage', {}).get('regions', []))}\n"

        # Add key metrics from metadata
        kpis = metadata.get('key_performance_metrics', {})
        financial = kpis.get('financial', {})
        expertise_context += f"\n=== KEY BUSINESS METRICS ===\n"
        expertise_context += f"Total Revenue: {financial.get('total_revenue', '₹682M')}\n"
        expertise_context += f"Avg Transaction Value: {financial.get('average_transaction_value', '₹365')}\n"
        expertise_context += f"Daily Revenue: {financial.get('daily_avg_revenue', '₹935K')}\n"

        # Add critical insights based on question type
        insights = metadata.get('detailed_insights', {})

        # Revenue insights
        if 'revenue' in state["question"].lower() or 'sales' in state["question"].lower():
            rev_perf = insights.get('revenue_performance', {})
            expertise_context += f"\n=== REVENUE INSIGHTS ===\n"
            expertise_context += f"Peak Month: {rev_perf.get('peak_month', 'May 2023')}\n"
            expertise_context += f"Variance: {rev_perf.get('variance', '18.6%')}\n"

        # Customer insights
        if 'customer' in state["question"].lower() or 'retention' in state["question"].lower():
            cust_seg = insights.get('customer_segmentation', {})
            expertise_context += f"\n=== CUSTOMER INSIGHTS ===\n"
            regular = cust_seg.get('regular_customers', {})
            premium = cust_seg.get('premium_customers', {})
            occasional = cust_seg.get('occasional_customers', {})
            expertise_context += f"Regular: {regular.get('count', '196K')} - {regular.get('strategy', '')}\n"
            expertise_context += f"Premium: {premium.get('avg_transaction', '₹418')} avg - {premium.get('strategy', '')}\n"
            expertise_context += f"Occasional: {occasional.get('opportunity', '₹60M potential')}\n"

        # Operational insights
        if 'staff' in state["question"].lower() or 'operational' in state["question"].lower() or 'hour' in state["question"].lower():
            ops = insights.get('operational_excellence', {})
            expertise_context += f"\n=== OPERATIONAL INSIGHTS ===\n"
            traffic = ops.get('hourly_traffic_pattern', {})
            expertise_context += f"Peak Time: Evening 4-9 PM (45% of traffic)\n"
            staffing = ops.get('staffing_optimization', {})
            expertise_context += f"Staffing Issue: {staffing.get('current_issue', '')}\n"
            expertise_context += f"Recommendation: {staffing.get('recommendation', '')}\n"
            expertise_context += f"Savings: {staffing.get('labor_cost_savings', '₹5-8M annually')}\n"

        # Wastage insights
        if 'wastage' in state["question"].lower() or 'perishable' in state["question"].lower():
            wastage = insights.get('inventory_wastage_control', {})
            expertise_context += f"\n=== WASTAGE CONTROL INSIGHTS ===\n"
            expertise_context += f"Estimated Wastage: {wastage.get('estimated_wastage_cost', '₹15-20M annually')}\n"
            expertise_context += f"Potential Savings: {wastage.get('potential_savings', '₹8-12M/year')}\n"
            perishables = wastage.get('perishable_categories', {})
            for cat, details in perishables.items():
                expertise_context += f"{cat.title()}: {details.get('action', '')}\n"

        # Add retail expertise knowledge
        retail_kb = metadata.get('retail_expertise_knowledge_base', {})
        expertise_context += f"\n=== RETAIL BEST PRACTICES ===\n"

        # Inventory management
        inv_mgmt = retail_kb.get('inventory_management_best_practices', {})
        if 'inventory' in state["question"].lower():
            expertise_context += f"ABC Analysis: {inv_mgmt.get('abc_analysis', '')}\n"
            expertise_context += f"Safety Stock: {inv_mgmt.get('safety_stock_formula', '')}\n"

        # Pricing
        pricing = retail_kb.get('pricing_psychology', {})
        if 'price' in state["question"].lower() or 'promotion' in state["question"].lower():
            expertise_context += f"Bundle Pricing: {pricing.get('bundle_pricing', '')}\n"
            expertise_context += f"Charm Pricing: {pricing.get('charm_pricing', '')}\n"

        # KPI Monitoring
        kpi_mon = retail_kb.get('kpi_monitoring', {})
        thresholds = kpi_mon.get('alert_thresholds', {})
        expertise_context += f"\n=== ALERT THRESHOLDS ===\n"
        for metric, threshold in thresholds.items():
            expertise_context += f"{metric}: {threshold}\n"

    # Load prompt template from file and inject context
    analysis_prompt = data_loader.prompt_template.format(
        expertise_context=expertise_context,
        data_context=state["loaded_context"],
        question=state["question"]
    )

    analysis = call_ollama(analysis_prompt)

    print(f"  ✓ Analysis generated with domain expertise ({len(analysis)} chars)")

    return Command(
        goto="verification_agent",
        update={"analysis": analysis, "facts_verified": False}
    )


# ===== AGENT 3: VERIFICATION =====
def verification_agent(state: StoreManagerState) -> Command[Literal[END]]:
    """
    VERIFICATION AGENT - Fact-checks analysis against data and CORRECTS errors
    """
    print("\n✅ VERIFICATION AGENT: Fact-checking and correcting analysis...")

    analysis = state["analysis"]
    context = state.get("loaded_context", "")

    # Extract store IDs mentioned in analysis
    store_ids = re.findall(r'STR_\d+', analysis)

    verified_analysis = analysis
    corrections_made = 0

    # If we have store performance data in context, verify and correct numbers
    if 'STORE PERFORMANCE DATA' in context and store_ids:
        print(f"  → Found {len(set(store_ids))} store references, verifying against data...")

        # Parse the actual data from context
        for store_id in set(store_ids):
            # Find the store's actual data in context
            # Look for patterns like "STR_002    Store Performance    14921921.76"
            pattern = rf'{store_id}\s+Store Performance\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)'
            match = re.search(pattern, context)

            if match:
                actual_revenue = float(match.group(1))
                actual_atv = float(match.group(2))
                actual_transactions = float(match.group(3))

                # Convert to human readable format
                revenue_m = actual_revenue / 1_000_000

                # Find and replace incorrect revenue mentions
                # Pattern: "STR_XXX - ₹XX.XM" or "STR_XXX (₹XX.XM"
                incorrect_patterns = [
                    rf'{store_id}\s*[-–]\s*₹[\d.]+M',
                    rf'{store_id}\s*\(₹[\d.]+M',
                    rf'{store_id}\s+generated\s+₹[\d.]+M',
                    rf'{store_id}\s+has\s+generated\s+₹[\d,.]+',
                ]

                for pattern in incorrect_patterns:
                    if re.search(pattern, verified_analysis):
                        # Replace with correct value
                        correct_value = f"{store_id} - ₹{revenue_m:.2f}M"
                        verified_analysis = re.sub(
                            rf'{store_id}\s*[-–]\s*₹[\d.]+M',
                            correct_value,
                            verified_analysis
                        )
                        verified_analysis = re.sub(
                            rf'{store_id}\s*\(₹[\d.]+M',
                            f"{store_id} (₹{revenue_m:.2f}M",
                            verified_analysis
                        )
                        verified_analysis = re.sub(
                            rf'{store_id}\s+generated\s+₹[\d,.]+\s+in\s+revenue',
                            f"{store_id} generated ₹{revenue_m:.2f}M in revenue",
                            verified_analysis
                        )
                        verified_analysis = re.sub(
                            rf'{store_id}\s+has\s+generated\s+₹[\d,.]+',
                            f"{store_id} has generated ₹{revenue_m:.2f}M",
                            verified_analysis
                        )
                        corrections_made += 1

                print(f"  ✓ Verified {store_id}: ₹{revenue_m:.2f}M revenue, {int(actual_transactions):,} transactions")

    # Extract numerical claims for reporting
    patterns = [
        r'₹[\d,]+\.?\d*[MKmk]?',
        r'\d+\.?\d*%',
        r'\d+[\d,]*\s+(customers|stores|products|transactions)',
    ]

    claims = []
    for pattern in patterns:
        matches = re.findall(pattern, verified_analysis, re.IGNORECASE)
        claims.extend(matches)

    claims = list(set(claims))[:10]  # Unique claims, limit to 10

    if corrections_made > 0:
        print(f"  ✓ Made {corrections_made} corrections to ensure accuracy")
        verified_analysis += f"\n\n*[{corrections_made} fact(s) verified and corrected against actual data]*"

    print(f"  ✓ {len(claims)} factual claims in final answer")

    return Command(
        goto=END,
        update={
            "extracted_claims": claims,
            "facts_verified": True,
            "verified_analysis": verified_analysis,
            "final_answer": verified_analysis
        }
    )


# ===== BUILD LANGGRAPH =====
def build_store_manager_graph():
    """Build the LangGraph StateGraph"""

    # Create graph
    builder = StateGraph(StoreManagerState)

    # Add agent nodes
    builder.add_node("router_agent", router_agent)
    builder.add_node("context_loader", context_loader)
    builder.add_node("analysis_agent", analysis_agent)
    builder.add_node("verification_agent", verification_agent)

    # Define flow
    builder.add_edge(START, "router_agent")
    # Agents use Command to route, no need for manual edges

    # Compile
    graph = builder.compile()

    return graph


# ===== MAIN SYSTEM =====
class LangGraphStoreManager:
    """LangGraph-based Multi-Agent Store Manager"""

    def __init__(self):
        self.graph = build_store_manager_graph()
        print("\n" + "="*70)
        print("LANGGRAPH MULTI-AGENT SYSTEM INITIALIZED")
        print("="*70)
        print("✓ Router Agent")
        print("✓ Context Loader")
        print("✓ Analysis Agent (Store Manager Persona)")
        print("✓ Verification Agent")
        print("✓ State Management via StateGraph")
        print("✓ Agent Communication via Command")
        print("="*70 + "\n")

    def ask(self, question: str) -> str:
        """Ask a question and get verified insights"""

        print("\n" + "="*70)
        print("LANGGRAPH MULTI-AGENT PIPELINE EXECUTING")
        print("="*70)

        # Initialize state
        initial_state = {
            "question": question,
            "data_sources": [],
            "analysis_type": "",
            "key_focus": "",
            "loaded_context": "",
            "analysis": "",
            "facts_verified": False,
            "extracted_claims": [],
            "verified_analysis": "",
            "final_answer": ""
        }

        # Run graph
        result = self.graph.invoke(initial_state)

        print("\n" + "="*70)
        print("PIPELINE COMPLETE")
        print("="*70 + "\n")

        return result["final_answer"]

    def run_interactive(self):
        """Interactive command-line interface"""
        print("\n" + "="*70)
        print("LANGGRAPH MULTI-AGENT STORE MANAGER")
        print("="*70)
        print("\n🤖 TRUE Multi-Agent Framework with LangGraph")
        print("📊 StateGraph orchestration with Command routing")
        print("💼 Store Manager Persona (15+ years experience)")
        print("\n💡 Ask strategic questions:")
        print("  • What are the top revenue opportunities?")
        print("  • How can we reduce perishable wastage?")
        print("  • Which customer segment should we prioritize?")
        print("\nType 'quit' or 'exit' to end.")
        print("="*70 + "\n")

        while True:
            try:
                question = input("\n🏪 You: ").strip()

                if not question:
                    continue

                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you for using LangGraph Store Manager!")
                    break

                # Get answer through LangGraph
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
            models = response.json().get('models', [])
            print(f"✓ Ollama connected")
            print(f"✓ Available models: {', '.join([m['name'] for m in models][:3])}")
        else:
            print("⚠ Ollama warning")
    except:
        print("\n❌ ERROR: Cannot connect to Ollama!")
        print("\nSetup:")
        print("  1. Install: https://ollama.ai")
        print("  2. Start: ollama serve")
        print("  3. Pull model: ollama pull llama3.2")
        sys.exit(1)

    # Create and run system
    system = LangGraphStoreManager()
    system.run_interactive()


if __name__ == "__main__":
    main()
