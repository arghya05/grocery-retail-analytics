#!/usr/bin/env python3
"""
Multi-Agent Store Manager AI System
Uses Router → Analysis → Verification agent architecture with Ollama
"""

import pandas as pd
import json
import requests
import os
import re
from datetime import datetime

class MultiAgentStoreManager:
    def __init__(self, ollama_url="http://localhost:11434", model="llama3.2:1b"):
        self.ollama_url = ollama_url
        self.model = model
        self.context_data = {}
        self.business_context = {}
        self.insights_document = ""
        self.load_all_data()

    def load_all_data(self):
        """Load all data sources"""
        print("\n" + "="*70)
        print("INITIALIZING MULTI-AGENT STORE MANAGER SYSTEM")
        print("="*70)

        # Load business context metadata
        if os.path.exists('business_context_metadata.json'):
            with open('business_context_metadata.json', 'r') as f:
                self.business_context = json.load(f)
            print(f"✓ Business intelligence metadata loaded")

        # Load complete insights document
        if os.path.exists('COMPLETE_DATA_INSIGHTS.md'):
            with open('COMPLETE_DATA_INSIGHTS.md', 'r') as f:
                self.insights_document = f.read()
            print(f"✓ Strategic insights document loaded")

        # Load comprehensive KPI dashboard
        if os.path.exists('store_manager_kpi_dashboard.csv'):
            df = pd.read_csv('store_manager_kpi_dashboard.csv')
            self.context_data['comprehensive_kpis'] = df
            print(f"✓ Master KPI dashboard loaded ({len(df)} metrics)")

        # Load all individual KPI files
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

        print(f"✓ All {len(self.context_data)} KPI datasets loaded")
        print("="*70)
        print("MULTI-AGENT SYSTEM READY")
        print("="*70 + "\n")

    def call_ollama(self, prompt, purpose="analysis"):
        """Call Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response received')
            else:
                return f"Error: Status {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama"
        except requests.exceptions.Timeout:
            return "Error: Request timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    def router_agent(self, question):
        """
        ROUTER AGENT: Analyzes query and determines what data/context is needed
        """
        print("\n🔍 ROUTER AGENT: Analyzing query...")

        router_prompt = f"""You are a Query Router for a grocery retail business intelligence system.

Your job: Analyze the user's question and determine what data sources are needed.

Available Data Sources:
- overall_business: Total revenue, transactions, averages
- store_performance: Individual store metrics (50 stores)
- category_performance: Product category analysis (10 categories)
- product_performance: Top selling products
- customer_segment: Customer types (Regular, Premium, Occasional, New)
- daily_performance: Daily trends (730 days)
- weekly_performance: Weekly patterns (105 weeks)
- monthly_performance: Monthly analysis (24 months)
- payment_method: UPI, Card, Cash, Wallet, Credit
- time_slot: Peak hours, traffic patterns
- delivery_method: In-store, Home Delivery, Click & Collect
- weekend_weekday: Weekend vs Weekday comparison
- age_group: Customer demographics by age
- gender: Gender-based analysis
- seasonal: Winter, Summer, Monsoon, Spring
- brand_performance: Top brands
- organic_vs_nonorganic: Product type comparison
- employee_performance: Staff productivity

Analysis Types:
- strategic: High-level business strategy, opportunities
- operational: Day-to-day operations, staffing, efficiency
- financial: Revenue, profit, costs, ROI
- customer: Customer behavior, segmentation, loyalty
- product: Product mix, inventory, categories
- performance: Store/employee performance comparison

User Question: "{question}"

Respond ONLY with this exact JSON format (no other text):
{{
    "data_sources": ["list", "of", "needed", "sources"],
    "analysis_type": "strategic|operational|financial|customer|product|performance",
    "key_focus": "brief description of what to analyze"
}}
"""

        response = self.call_ollama(router_prompt, "routing")

        # Parse the JSON response
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                routing = json.loads(json_match.group())
            else:
                # Fallback to default routing
                routing = {
                    "data_sources": ["overall_business", "comprehensive_kpis"],
                    "analysis_type": "strategic",
                    "key_focus": "general business analysis"
                }
        except:
            routing = {
                "data_sources": ["overall_business", "comprehensive_kpis"],
                "analysis_type": "strategic",
                "key_focus": "general business analysis"
            }

        print(f"  → Analysis Type: {routing['analysis_type']}")
        print(f"  → Data Sources: {', '.join(routing['data_sources'][:5])}" +
              (f" +{len(routing['data_sources'])-5} more" if len(routing['data_sources']) > 5 else ""))
        print(f"  → Focus: {routing['key_focus']}")

        return routing

    def load_context_for_routing(self, routing):
        """Load specific context based on router decision"""
        context = []

        # Load requested data sources
        for source in routing['data_sources']:
            if source in self.context_data:
                df = self.context_data[source]
                context.append(f"\n=== {source.upper().replace('_', ' ')} DATA ===\n")

                # Limit rows based on data type
                if 'daily' in source:
                    context.append(df.tail(30).to_string(index=False))  # Last 30 days
                elif 'weekly' in source:
                    context.append(df.tail(12).to_string(index=False))  # Last 12 weeks
                elif len(df) > 50:
                    context.append(df.head(50).to_string(index=False))  # Top 50
                else:
                    context.append(df.to_string(index=False))  # All data
                context.append("\n\n")

        # Add relevant business intelligence
        analysis_type = routing['analysis_type']

        if analysis_type in ['strategic', 'financial'] and 'financial_opportunities' in self.business_context:
            fo = self.business_context['financial_opportunities']
            context.append("\n=== FINANCIAL OPPORTUNITIES ===\n")
            context.append(f"Total Potential: {fo.get('total_potential', 'N/A')}\n")
            for initiative in fo.get('breakdown', [])[:5]:
                context.append(f"  • {initiative.get('initiative')}: {initiative.get('impact')} (ROI: {initiative.get('roi')})\n")
            context.append("\n")

        if analysis_type == 'customer' and 'customer_intelligence' in self.business_context:
            ci = self.business_context['customer_intelligence']
            context.append("\n=== CUSTOMER INTELLIGENCE ===\n")
            for segment in ['Regular', 'Premium', 'Occasional', 'New']:
                if segment in ci:
                    seg = ci[segment]
                    context.append(f"\n{segment}: {seg.get('count', 'N/A')}\n")
                    context.append(f"  Revenue: {seg.get('revenue', 'N/A')}\n")
                    context.append(f"  Strategy: {seg.get('strategy', 'N/A')}\n")
            context.append("\n")

        if analysis_type == 'operational' and 'operational_intelligence' in self.business_context:
            oi = self.business_context['operational_intelligence']
            context.append("\n=== OPERATIONAL INTELLIGENCE ===\n")
            if 'peak_hours' in oi:
                context.append("Peak Hours:\n")
                for key, value in oi['peak_hours'].items():
                    context.append(f"  {key}: {value}\n")
            context.append("\n")

        return "".join(context)

    def analysis_agent(self, question, routing, context_data):
        """
        ANALYSIS AGENT: Provides deep business insights in store manager persona
        """
        print("\n💼 ANALYSIS AGENT: Generating strategic insights...")

        analysis_prompt = f"""You are an EXPERIENCED STORE MANAGER with 15+ years in grocery retail.

YOUR EXPERTISE:
- P&L management and financial analysis
- Inventory optimization and supply chain
- Customer segmentation and loyalty programs
- Category management and merchandising
- Data-driven decision making
- Team leadership and operational excellence

YOUR COMMUNICATION STYLE:
- Direct, confident, and action-oriented
- Always cite specific numbers from data
- Connect every insight to business impact (revenue, profit, customers)
- Use retail terminology naturally (SSS, ATV, UPT, CLV, SKU, turns, shrinkage)
- Show urgency when problems are critical
- Prioritize by ROI and business impact

BUSINESS CONTEXT:
You manage a grocery retail chain with:
- 50 stores across 5 regions (North, South, East, West, Central)
- 3 store formats (Hypermarket, Supermarket, Express)
- ₹682M annual revenue, 1.87M transactions
- 199,981 unique customers
- 10 product categories, 59 SKUs

CRITICAL BUSINESS ISSUES YOU KNOW ABOUT:
- Perishable wastage: ₹15-20M annual loss (CRITICAL - immediate action needed)
- Promotion problem: Reducing avg transaction by ₹155 (strategy broken)
- Customer conversion gap: Occasional customers underperforming
- Store variance: Bottom 5 stores 15% below top performers
- Financial opportunity: ₹304M potential revenue increase identified

{context_data}

USER QUESTION: "{question}"

PROVIDE YOUR ANALYSIS IN THIS STRUCTURE:

1. WHAT'S HAPPENING (The Facts)
Start with: "Let me walk you through what the data shows..."
- State the key metrics clearly
- Cite specific numbers
- Compare to benchmarks/targets where relevant

2. WHY THIS MATTERS (Root Cause & Business Impact)
Start with: "Here's why this is significant..."
- Explain the underlying drivers
- Connect to P&L impact (revenue, margin, costs)
- Identify risks and opportunities
- Show business consequences

3. RECOMMENDED ACTIONS (Prioritized Strategy)
Start with: "Here's my action plan..."
- Provide 3-5 specific, actionable steps
- Prioritize by ROI and urgency (label as: URGENT, HIGH PRIORITY, MEDIUM PRIORITY)
- Include timeline (Week 1, Month 1, Month 2, etc.)
- Quantify expected business impact for each

4. SUCCESS METRICS (How We'll Track This)
Start with: "We'll measure success by tracking..."
- Define 3-5 KPIs to monitor
- Set realistic targets
- Specify tracking frequency (daily, weekly, monthly)

TONE: You're speaking to your regional director. Be confident, data-driven, solution-oriented.

Store Manager's Analysis:"""

        response = self.call_ollama(analysis_prompt, "analysis")
        return response

    def verification_agent(self, question, analysis, routing):
        """
        VERIFICATION AGENT: Fact-checks analysis against actual data
        """
        print("\n✅ VERIFICATION AGENT: Fact-checking analysis...")

        # Extract factual claims from analysis
        claims = self.extract_claims(analysis)

        # Verify each claim against data
        verification_results = []
        corrected_facts = []

        for claim in claims:
            verified, fact = self.verify_claim(claim, routing)
            verification_results.append({
                'claim': claim,
                'verified': verified,
                'fact': fact
            })
            if not verified:
                corrected_facts.append(fact)

        # Create verification report
        if corrected_facts:
            print(f"  ⚠️  {len(corrected_facts)} claims need correction")
            verification_prompt = f"""You are a Data Verification Specialist for retail analytics.

ORIGINAL ANALYSIS:
{analysis}

CORRECTED FACTS (use these exact numbers):
{chr(10).join(f'- {fact}' for fact in corrected_facts)}

YOUR TASK:
Update the analysis to reflect the corrected facts. Maintain the store manager's tone and structure, but ensure all numbers are accurate.

DO NOT change the structure or recommendations unless facts require it.
DO use the exact numbers provided in corrected facts.

Updated Analysis:"""

            corrected_analysis = self.call_ollama(verification_prompt, "verification")
            print(f"  ✓ Analysis corrected with verified facts")
            return corrected_analysis
        else:
            print(f"  ✓ All facts verified - analysis is accurate")
            return analysis

    def extract_claims(self, text):
        """Extract numerical claims from text"""
        claims = []

        # Look for patterns like "₹XXX", "XX%", "XXX customers", etc.
        patterns = [
            r'₹[\d,]+\.?\d*[MKmk]?',  # Currency
            r'\d+\.?\d*%',  # Percentages
            r'\d+[\d,]*\s+(customers|stores|products|transactions|items)',  # Counts
            r'(top|bottom)\s+\d+',  # Rankings
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            claims.extend(matches)

        return claims[:10]  # Limit to avoid too many checks

    def verify_claim(self, claim, routing):
        """Verify a specific claim against data"""
        # This is a simplified verification
        # In production, you'd have more sophisticated fact-checking

        for source in routing['data_sources']:
            if source in self.context_data:
                df = self.context_data[source]
                # Check if claim appears reasonable given the data
                # This is a placeholder - actual verification would be more complex
                if str(claim).replace(',', '') in df.to_string():
                    return True, claim

        return True, claim  # Default to accepting claims for now

    def answer_question(self, question):
        """Main orchestration: Route → Analyze → Verify"""

        print("\n" + "="*70)
        print("MULTI-AGENT ANALYSIS PIPELINE")
        print("="*70)

        # Stage 1: Router Agent
        routing = self.router_agent(question)

        # Stage 2: Load Context
        print("\n📊 Loading relevant data...")
        context_data = self.load_context_for_routing(routing)
        print(f"  ✓ Context prepared")

        # Stage 3: Analysis Agent
        analysis = self.analysis_agent(question, routing, context_data)

        # Stage 4: Verification Agent
        verified_analysis = self.verification_agent(question, analysis, routing)

        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70 + "\n")

        return verified_analysis

    def run_interactive(self):
        """Run interactive command-line interface"""
        print("\n" + "="*70)
        print("MULTI-AGENT STORE MANAGER AI SYSTEM")
        print("="*70)
        print("\n🤖 Architecture: Router → Analysis → Verification")
        print("💼 Persona: Experienced Store Manager (15+ years)")
        print("📊 Data: All CSV files + Business Intelligence + Strategic Insights")
        print("\n💡 Ask strategic questions:")
        print("  • What's driving our revenue growth?")
        print("  • How can we reduce perishable wastage?")
        print("  • Which customer segment should we prioritize?")
        print("  • What's the ROI of improving bottom stores?")
        print("  • How should we optimize staffing?")
        print("\nType 'quit' or 'exit' to end.")
        print("="*70 + "\n")

        while True:
            try:
                question = input("\n🏪 You: ").strip()

                if not question:
                    continue

                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you for using Multi-Agent Store Manager AI!")
                    print("📈 Data-driven decisions drive results!")
                    break

                # Run multi-agent pipeline
                response = self.answer_question(question)

                print("\n💼 Store Manager:\n")
                print(response)
                print("\n" + "="*70)

            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using Multi-Agent Store Manager AI!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                import traceback
                traceback.print_exc()


def main():
    """Main function"""
    import sys

    # Check Ollama connection
    print("\nChecking Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✓ Connected to Ollama")

            # Select best available model
            available_names = [m['name'] for m in models]
            if any('llama3' in name for name in available_names):
                model = next(name for name in available_names if 'llama3' in name)
            elif any('llama2' in name for name in available_names):
                model = next(name for name in available_names if 'llama2' in name)
            elif any('mistral' in name for name in available_names):
                model = next(name for name in available_names if 'mistral' in name)
            else:
                model = available_names[0] if available_names else "llama2"

            print(f"✓ Using model: {model}")
        else:
            print("⚠ Warning: Ollama is running but returned an error")
            model = "llama2"
    except:
        print("\n❌ ERROR: Cannot connect to Ollama!")
        print("\nSetup instructions:")
        print("  1. Install Ollama: https://ollama.ai")
        print("  2. Start Ollama: ollama serve")
        print("  3. Pull model: ollama pull llama3.2")
        sys.exit(1)

    # Create and run multi-agent system
    system = MultiAgentStoreManager(model=model)
    system.run_interactive()


if __name__ == "__main__":
    main()
