#!/usr/bin/env python3
"""
Enhanced Store Manager AI Assistant
Uses Ollama with comprehensive business context to provide deep insights
"""

import pandas as pd
import json
import requests
import os
from datetime import datetime

class EnhancedStoreManagerAssistant:
    def __init__(self, ollama_url="http://localhost:11434", model="llama2"):
        self.ollama_url = ollama_url
        self.model = model
        self.context_data = {}
        self.business_context = {}
        self.insights_document = ""
        self.load_all_data()

    def load_all_data(self):
        """Load all data sources: KPIs, business context, insights"""
        print("\n" + "="*70)
        print("LOADING COMPREHENSIVE BUSINESS INTELLIGENCE")
        print("="*70)

        # Load business context metadata
        if os.path.exists('business_context_metadata.json'):
            with open('business_context_metadata.json', 'r') as f:
                self.business_context = json.load(f)
            print(f"✓ Loaded business context metadata")

        # Load complete insights document
        if os.path.exists('COMPLETE_DATA_INSIGHTS.md'):
            with open('COMPLETE_DATA_INSIGHTS.md', 'r') as f:
                self.insights_document = f.read()
            print(f"✓ Loaded complete data insights document")

        # Load the comprehensive KPI dashboard
        if os.path.exists('store_manager_kpi_dashboard.csv'):
            df = pd.read_csv('store_manager_kpi_dashboard.csv')
            self.context_data['comprehensive_kpis'] = df
            print(f"✓ Loaded comprehensive KPI dashboard: {len(df)} KPIs")

        # Load individual KPI files - ALL OF THEM
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

        print(f"✓ Loaded {len(self.context_data)} KPI datasets")
        print("="*70)
        print("READY TO PROVIDE BUSINESS INSIGHTS")
        print("="*70 + "\n")

    def build_business_context(self):
        """Build rich business context from metadata"""
        context = []

        context.append("=== YOUR ROLE ===\n")
        context.append("You are an experienced grocery store manager with 15+ years in retail operations.\n")
        context.append("Your expertise: P&L management, inventory optimization, customer segmentation, merchandising.\n")
        context.append("Your style: Data-driven, actionable, business-focused, uses retail terminology naturally.\n\n")

        # Business Overview
        if 'business_overview' in self.business_context:
            bo = self.business_context['business_overview']
            context.append("=== BUSINESS OVERVIEW ===\n")
            context.append(f"Company: {bo.get('company_type', 'Multi-store Retail Chain')}\n")
            context.append(f"Network: {bo.get('total_stores', '50')} stores across {len(bo.get('geographic_presence', []))} regions\n")
            context.append(f"Annual Revenue: {bo.get('annual_revenue', '₹682.3M')}\n")
            context.append(f"Customer Base: {bo.get('customer_base', '200K customers')}\n")
            context.append(f"Data Period: {bo.get('data_period', '24 months')}\n\n")

        # Critical Insights
        if 'critical_insights' in self.business_context:
            ci = self.business_context['critical_insights']

            context.append("=== CRITICAL BUSINESS INSIGHTS ===\n\n")

            context.append("STRENGTHS:\n")
            for strength in ci.get('strengths', [])[:3]:
                context.append(f"✓ {strength}\n")
            context.append("\n")

            context.append("OPPORTUNITIES (Quick Wins):\n")
            for opp in ci.get('quick_wins', [])[:3]:
                context.append(f"💡 {opp}\n")
            context.append("\n")

            context.append("KEY CHALLENGES:\n")
            for threat in ci.get('threats', [])[:3]:
                context.append(f"⚠️ {threat}\n")
            context.append("\n")

        # Key Performance Metrics
        if 'comprehensive_kpis' in self.context_data:
            df = self.context_data['comprehensive_kpis']
            overall = df[df['Section'] == 'Overall Business']

            context.append("=== KEY METRICS ===\n")
            for _, row in overall.head(8).iterrows():
                context.append(f"{row['KPI']}: {row['Value']}\n")
            context.append("\n")

        # Category Intelligence
        if 'category_intelligence' in self.business_context:
            ci = self.business_context['category_intelligence']
            context.append("=== CATEGORY INSIGHTS ===\n")
            for category in ['Beverages', 'Fresh Produce', 'Staples & Grains']:
                if category in ci:
                    cat_info = ci[category]
                    context.append(f"\n{category}: {cat_info.get('revenue', 'N/A')} ({cat_info.get('share', 'N/A')})\n")
                    if 'strategy' in cat_info:
                        context.append(f"  Strategy: {cat_info['strategy']}\n")
            context.append("\n")

        # Customer Intelligence
        if 'customer_intelligence' in self.business_context:
            ci = self.business_context['customer_intelligence']
            context.append("=== CUSTOMER SEGMENT INTELLIGENCE ===\n")
            for segment in ['Regular', 'Premium', 'Occasional']:
                if segment in ci:
                    seg_info = ci[segment]
                    context.append(f"\n{segment} Customers:\n")
                    context.append(f"  Count: {seg_info.get('count', 'N/A')}\n")
                    context.append(f"  Revenue: {seg_info.get('revenue', 'N/A')}\n")
                    context.append(f"  Avg Transaction: {seg_info.get('avg_transaction', 'N/A')}\n")
                    context.append(f"  Strategy: {seg_info.get('strategy', 'N/A')}\n")
            context.append("\n")

        return "".join(context)

    def get_specific_context(self, question):
        """Extract relevant context based on question keywords"""
        question_lower = question.lower()
        relevant_context = []

        # Check for topic-specific insights from business context
        if 'inventory_intelligence' in self.business_context and any(word in question_lower for word in ['inventory', 'stock', 'wastage', 'perishable']):
            ii = self.business_context['inventory_intelligence']
            relevant_context.append("\n=== INVENTORY INTELLIGENCE ===\n")
            if 'perishable_management' in ii:
                pm = ii['perishable_management']
                relevant_context.append(f"Wastage Cost: {pm.get('wastage_cost', 'N/A')}\n")
                relevant_context.append(f"Potential Savings: {pm.get('potential_savings', 'N/A')}\n")
                for key, value in pm.items():
                    if key not in ['wastage_cost', 'potential_savings']:
                        relevant_context.append(f"  {key}: {value}\n")
            relevant_context.append("\n")

        if 'pricing_intelligence' in self.business_context and any(word in question_lower for word in ['price', 'discount', 'promotion', 'margin']):
            pi = self.business_context['pricing_intelligence']
            relevant_context.append("\n=== PRICING & PROMOTION INTELLIGENCE ===\n")
            if 'discount_problem' in pi:
                dp = pi['discount_problem']
                relevant_context.append(f"CRITICAL ISSUE: {dp.get('issue', 'N/A')}\n")
                relevant_context.append(f"Current Promo Avg: {dp.get('current_promo_avg', 'N/A')}\n")
                relevant_context.append(f"Non-Promo Avg: {dp.get('non_promo_avg', 'N/A')}\n")
                relevant_context.append(f"Solution: {dp.get('solution', 'N/A')}\n")
                relevant_context.append(f"Expected Impact: {dp.get('expected_impact', 'N/A')}\n")
            relevant_context.append("\n")

        if 'seasonal_intelligence' in self.business_context and any(word in question_lower for word in ['season', 'winter', 'summer', 'monsoon', 'spring']):
            si = self.business_context['seasonal_intelligence']
            relevant_context.append("\n=== SEASONAL INTELLIGENCE ===\n")
            for season in ['Winter', 'Summer', 'Monsoon']:
                if season in si:
                    season_info = si[season]
                    relevant_context.append(f"\n{season}:\n")
                    for key, value in season_info.items():
                        relevant_context.append(f"  {key}: {value}\n")
            relevant_context.append("\n")

        if 'operational_intelligence' in self.business_context and any(word in question_lower for word in ['staff', 'hour', 'peak', 'checkout', 'operation']):
            oi = self.business_context['operational_intelligence']
            relevant_context.append("\n=== OPERATIONAL INTELLIGENCE ===\n")
            if 'peak_hours' in oi:
                ph = oi['peak_hours']
                for key, value in ph.items():
                    relevant_context.append(f"{key}: {value}\n")
            relevant_context.append("\n")

        if 'financial_opportunities' in self.business_context and any(word in question_lower for word in ['revenue', 'growth', 'opportunity', 'improve', 'increase']):
            fo = self.business_context['financial_opportunities']
            relevant_context.append("\n=== FINANCIAL OPPORTUNITIES ===\n")
            relevant_context.append(f"Total Potential: {fo.get('total_potential', 'N/A')}\n\n")
            relevant_context.append("Top Initiatives:\n")
            for initiative in fo.get('breakdown', [])[:5]:
                relevant_context.append(f"  - {initiative.get('initiative', 'N/A')}: {initiative.get('impact', 'N/A')} (ROI: {initiative.get('roi', 'N/A')})\n")
            relevant_context.append("\n")

        # Add relevant KPI data
        if any(word in question_lower for word in ['store', 'location', 'branch', 'region']):
            if 'store_performance' in self.context_data:
                df = self.context_data['store_performance']
                relevant_context.append("\n=== STORE PERFORMANCE DATA ===\n")
                relevant_context.append(df.head(10).to_string(index=False))
                relevant_context.append("\n\n")

        if any(word in question_lower for word in ['category', 'categories', 'product line']):
            if 'category_performance' in self.context_data:
                df = self.context_data['category_performance']
                relevant_context.append("\n=== CATEGORY PERFORMANCE DATA ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n\n")

        if any(word in question_lower for word in ['product', 'item', 'sku', 'top selling']):
            if 'product_performance' in self.context_data:
                df = self.context_data['product_performance']
                relevant_context.append("\n=== TOP PRODUCTS DATA ===\n")
                relevant_context.append(df.head(15).to_string(index=False))
                relevant_context.append("\n\n")

        if any(word in question_lower for word in ['customer', 'segment', 'loyalty', 'demographic']):
            if 'customer_segment' in self.context_data:
                df = self.context_data['customer_segment']
                relevant_context.append("\n=== CUSTOMER SEGMENT DATA ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n\n")

        if any(word in question_lower for word in ['daily', 'day', 'date', 'trend', 'pattern']):
            if 'daily_performance' in self.context_data:
                df = self.context_data['daily_performance']
                relevant_context.append("\n=== DAILY PERFORMANCE DATA (Recent) ===\n")
                relevant_context.append(df.tail(30).to_string(index=False))  # Last 30 days
                relevant_context.append("\n\n")

        if any(word in question_lower for word in ['week', 'weekly']):
            if 'weekly_performance' in self.context_data:
                df = self.context_data['weekly_performance']
                relevant_context.append("\n=== WEEKLY PERFORMANCE DATA (Recent) ===\n")
                relevant_context.append(df.tail(12).to_string(index=False))  # Last 12 weeks
                relevant_context.append("\n\n")

        if any(word in question_lower for word in ['master', 'summary', 'overview', 'dashboard']):
            if 'master_dashboard' in self.context_data:
                df = self.context_data['master_dashboard']
                relevant_context.append("\n=== MASTER DASHBOARD ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n\n")

        return "".join(relevant_context)

    def ask_ollama(self, question):
        """Send question to Ollama with comprehensive business context"""

        # Build comprehensive context
        business_context = self.build_business_context()
        specific_context = self.get_specific_context(question)

        # Create enhanced prompt
        prompt = f"""{business_context}

{specific_context}

=== YOUR TASK ===

As an experienced store manager, answer the following question with deep business insight.

RESPONSE STRUCTURE:
1. WHAT'S HAPPENING (Facts & Numbers)
   - State the key metrics clearly
   - Cite specific numbers from the data

2. WHY THIS MATTERS (Business Analysis)
   - Explain root causes and patterns
   - Connect to business impact (revenue, profit, customers)
   - Identify risks and opportunities

3. RECOMMENDED ACTIONS (Prioritized Steps)
   - Provide specific, actionable recommendations
   - Prioritize by ROI and urgency
   - Include expected business impact

4. SUCCESS METRICS (KPIs to Track)
   - Define how to measure success
   - Set realistic targets

TONE: Direct, confident, data-driven. Use business terminology naturally.
FOCUS: Always connect insights to business outcomes.

Question: {question}

Store Manager's Analysis:"""

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
                return f"Error: Ollama returned status code {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running (ollama serve)"
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Try a more specific question."
        except Exception as e:
            return f"Error: {str(e)}"

    def run_interactive(self):
        """Run interactive command-line interface"""
        print("\n" + "="*70)
        print("ENHANCED STORE MANAGER AI ASSISTANT")
        print("="*70)
        print("\n💼 I'm your AI Store Manager with deep retail intelligence.")
        print("📊 I have access to comprehensive business insights and 143 KPIs.")
        print("🎯 I provide actionable recommendations with business impact.")
        print("\n💡 Example questions:")
        print("  • What's driving our revenue growth?")
        print("  • Why is beverage performance so strong?")
        print("  • How can we reduce perishable wastage?")
        print("  • Which customer segment should we prioritize?")
        print("  • What's the ROI of improving bottom stores?")
        print("  • How should we adjust for seasonal demand?")
        print("\nType 'quit' or 'exit' to end the session.")
        print("="*70 + "\n")

        while True:
            try:
                question = input("\n🏪 You: ").strip()

                if not question:
                    continue

                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thanks for using Enhanced Store Manager AI!")
                    print("📈 Remember: Data-driven decisions drive results!")
                    break

                print("\n⏳ Analyzing business data and generating insights...\n")
                print("="*70)

                response = self.ask_ollama(question)

                print("\n💼 Store Manager:\n")
                print(response)
                print("\n" + "="*70)

            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using Enhanced Store Manager AI!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")


def main():
    """Main function"""
    import sys

    # Check if Ollama is accessible
    print("\nChecking Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✓ Connected to Ollama")
            print(f"✓ Available models: {', '.join([m['name'] for m in models])}")

            # Select model
            model = "llama2"
            if models:
                available_names = [m['name'] for m in models]
                if any('llama3' in name for name in available_names):
                    model = next(name for name in available_names if 'llama3' in name)
                elif any('llama2' in name for name in available_names):
                    model = next(name for name in available_names if 'llama2' in name)
                elif any('mistral' in name for name in available_names):
                    model = next(name for name in available_names if 'mistral' in name)
                else:
                    model = available_names[0]
                print(f"✓ Using model: {model}")
        else:
            print("⚠ Warning: Ollama is running but returned an error")
            model = "llama2"
    except:
        print("\n❌ ERROR: Cannot connect to Ollama!")
        print("\nPlease make sure Ollama is installed and running:")
        print("  1. Install Ollama from: https://ollama.ai")
        print("  2. Start Ollama: ollama serve")
        print("  3. Pull a model: ollama pull llama3")
        print("\nThen run this script again.")
        sys.exit(1)

    # Create and run enhanced assistant
    assistant = EnhancedStoreManagerAssistant(model=model)
    assistant.run_interactive()


if __name__ == "__main__":
    main()
