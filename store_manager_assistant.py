#!/usr/bin/env python3
"""
Store Manager AI Assistant
Uses Ollama to provide insights about grocery store data
"""

import pandas as pd
import json
import requests
import os
import glob
from datetime import datetime

class StoreManagerAssistant:
    def __init__(self, ollama_url="http://localhost:11434", model="llama2"):
        self.ollama_url = ollama_url
        self.model = model
        self.context_data = {}
        self.load_all_kpis()

    def load_all_kpis(self):
        """Load all KPI CSV files into memory"""
        print("\n" + "="*70)
        print("LOADING STORE DATA...")
        print("="*70)

        # Load the comprehensive KPI dashboard
        if os.path.exists('store_manager_kpi_dashboard.csv'):
            df = pd.read_csv('store_manager_kpi_dashboard.csv')
            self.context_data['comprehensive_kpis'] = df
            print(f"✓ Loaded comprehensive KPI dashboard: {len(df)} KPIs")

        # Load individual KPI files
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
            'employee_performance': 'kpi_employee_performance.csv'
        }

        for key, filename in kpi_files.items():
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                self.context_data[key] = df
                print(f"✓ Loaded {filename}")

        print("="*70)
        print(f"Total datasets loaded: {len(self.context_data)}")
        print("="*70 + "\n")

    def build_context_summary(self):
        """Build a comprehensive context summary for the LLM"""
        context = []

        context.append("=== STORE MANAGER CONTEXT ===\n")
        context.append("You are an experienced store manager analyzing grocery store chain data.\n")
        context.append("You have access to comprehensive business intelligence data.\n\n")

        # Overall Business Metrics
        if 'comprehensive_kpis' in self.context_data:
            df = self.context_data['comprehensive_kpis']

            # Overall Business
            overall = df[df['Section'] == 'Overall Business']
            context.append("=== OVERALL BUSINESS PERFORMANCE ===\n")
            for _, row in overall.iterrows():
                context.append(f"{row['KPI']}: {row['Value']}\n")
            context.append("\n")

            # Top Performers
            top = df[df['Section'] == 'Top Performers']
            context.append("=== TOP PERFORMERS ===\n")
            for _, row in top.iterrows():
                context.append(f"{row['KPI']}: {row['Value']}\n")
            context.append("\n")

            # Store Performance Summary
            store_perf = df[df['Section'] == 'Store Performance']
            context.append("=== STORE PERFORMANCE ===\n")
            for _, row in store_perf.head(6).iterrows():
                context.append(f"{row['KPI']}: {row['Value']}\n")
            context.append("\n")

            # Customer Insights Summary
            customer = df[df['Section'] == 'Customer Insights']
            context.append("=== CUSTOMER INSIGHTS ===\n")
            for _, row in customer.head(12).iterrows():
                context.append(f"{row['KPI']}: {row['Value']}\n")
            context.append("\n")

            # Operational Metrics Summary
            ops = df[df['Section'] == 'Operational Metrics']
            context.append("=== OPERATIONAL METRICS ===\n")
            for _, row in ops.head(10).iterrows():
                context.append(f"{row['KPI']}: {row['Value']}\n")
            context.append("\n")

            # Time-Based Trends Summary
            time = df[df['Section'] == 'Time-Based Trends']
            context.append("=== TIME-BASED TRENDS ===\n")
            for _, row in time.head(8).iterrows():
                context.append(f"{row['KPI']}: {row['Value']}\n")
            context.append("\n")

        return "".join(context)

    def get_specific_context(self, question):
        """Extract relevant context based on the question"""
        question_lower = question.lower()
        relevant_context = []

        # Check which datasets are relevant
        if any(word in question_lower for word in ['store', 'location', 'branch', 'region']):
            if 'store_performance' in self.context_data:
                df = self.context_data['store_performance']
                relevant_context.append("\n=== DETAILED STORE PERFORMANCE ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['category', 'categories', 'product line']):
            if 'category_performance' in self.context_data:
                df = self.context_data['category_performance']
                relevant_context.append("\n=== CATEGORY PERFORMANCE ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['product', 'item', 'sku', 'top selling']):
            if 'product_performance' in self.context_data:
                df = self.context_data['product_performance']
                relevant_context.append("\n=== TOP PRODUCTS ===\n")
                relevant_context.append(df.head(20).to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['customer', 'segment', 'age', 'gender', 'demographic']):
            if 'customer_segment' in self.context_data:
                df = self.context_data['customer_segment']
                relevant_context.append("\n=== CUSTOMER SEGMENTS ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")
            if 'age_group' in self.context_data:
                df = self.context_data['age_group']
                relevant_context.append("\n=== AGE GROUP ANALYSIS ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['time', 'hour', 'peak', 'busy', 'slot', 'when']):
            if 'time_slot' in self.context_data:
                df = self.context_data['time_slot']
                relevant_context.append("\n=== TIME SLOT PERFORMANCE ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['weekend', 'weekday', 'day']):
            if 'weekend_weekday' in self.context_data:
                df = self.context_data['weekend_weekday']
                relevant_context.append("\n=== WEEKEND VS WEEKDAY ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['season', 'seasonal', 'winter', 'summer', 'spring', 'monsoon']):
            if 'seasonal' in self.context_data:
                df = self.context_data['seasonal']
                relevant_context.append("\n=== SEASONAL PERFORMANCE ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['payment', 'upi', 'cash', 'card', 'wallet']):
            if 'payment_method' in self.context_data:
                df = self.context_data['payment_method']
                relevant_context.append("\n=== PAYMENT METHODS ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['delivery', 'home', 'click', 'collect', 'online']):
            if 'delivery_method' in self.context_data:
                df = self.context_data['delivery_method']
                relevant_context.append("\n=== DELIVERY METHODS ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['brand', 'manufacturer', 'supplier']):
            if 'brand_performance' in self.context_data:
                df = self.context_data['brand_performance']
                relevant_context.append("\n=== BRAND PERFORMANCE ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['organic', 'non-organic', 'natural']):
            if 'organic_vs_nonorganic' in self.context_data:
                df = self.context_data['organic_vs_nonorganic']
                relevant_context.append("\n=== ORGANIC VS NON-ORGANIC ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['employee', 'staff', 'checkout', 'cashier']):
            if 'employee_performance' in self.context_data:
                df = self.context_data['employee_performance']
                relevant_context.append("\n=== EMPLOYEE PERFORMANCE ===\n")
                relevant_context.append(df.head(20).to_string(index=False))
                relevant_context.append("\n")

        if any(word in question_lower for word in ['month', 'monthly', 'trend']):
            if 'monthly_performance' in self.context_data:
                df = self.context_data['monthly_performance']
                relevant_context.append("\n=== MONTHLY PERFORMANCE ===\n")
                relevant_context.append(df.to_string(index=False))
                relevant_context.append("\n")

        return "".join(relevant_context)

    def ask_ollama(self, question):
        """Send question to Ollama and get response"""

        # Build the full context
        base_context = self.build_context_summary()
        specific_context = self.get_specific_context(question)

        # Create the prompt
        prompt = f"""You are an experienced grocery store manager with deep business intelligence expertise.
You are analyzing data from a grocery store chain to provide actionable insights.

{base_context}

{specific_context}

Based on the data above, answer the following question as a store manager would.
Provide insights on:
1. WHAT happened (the facts and numbers)
2. WHY it happened (the underlying reasons and patterns)
3. WHAT should be done (actionable recommendations)

Be specific, use numbers from the data, and think like a business leader.

Question: {question}

Store Manager's Analysis:"""

        try:
            # Call Ollama API
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
            return "Error: Request timed out. The question might be too complex."
        except Exception as e:
            return f"Error: {str(e)}"

    def run_interactive(self):
        """Run interactive command-line interface"""
        print("\n" + "="*70)
        print("STORE MANAGER AI ASSISTANT")
        print("="*70)
        print("\nAsk me anything about the store's performance!")
        print("I'll analyze the data and provide insights on what happened and why.")
        print("\nExample questions:")
        print("  - What are our top performing stores?")
        print("  - Why is the beverage category performing so well?")
        print("  - Which customer segment should we focus on?")
        print("  - What time of day should we increase staffing?")
        print("  - How can we improve weekend sales?")
        print("\nType 'quit' or 'exit' to end the session.")
        print("="*70 + "\n")

        while True:
            try:
                question = input("\n🏪 You: ").strip()

                if not question:
                    continue

                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you for using Store Manager AI Assistant!")
                    break

                print("\n⏳ Analyzing data and generating insights...\n")
                print("="*70)

                response = self.ask_ollama(question)

                print("\n📊 Store Manager:\n")
                print(response)
                print("\n" + "="*70)

            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using Store Manager AI Assistant!")
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
                # Try to use llama3 if available, otherwise use first available model
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
        print("  3. Pull a model: ollama pull llama2")
        print("\nThen run this script again.")
        sys.exit(1)

    # Create and run assistant
    assistant = StoreManagerAssistant(model=model)
    assistant.run_interactive()


if __name__ == "__main__":
    main()
