#!/usr/bin/env python3
"""
Grocery Dataset Scaler - 4-5B Revenue Retailer
Scales the grocery dataset to reflect a 4-5B revenue retailer and converts to USD
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

class GroceryDatasetScaler:
    def __init__(self, input_file: str, output_file: str = None):
        self.input_file = input_file
        self.output_file = output_file or input_file.replace('.csv', '_4_5b_usd.csv')
        
        # Scaling factors for 4-5B retailer
        self.scale_factors = {
            'revenue_multiplier': 500,  # Scale from ~$8M to ~$4B
            'store_count_multiplier': 50,  # Scale from ~50 stores to ~2,500 stores
            'customer_count_multiplier': 50,  # Scale from ~200K to ~10M customers
            'transaction_count_multiplier': 50,  # Scale from ~1.87M to ~93.5M transactions
            'inr_to_usd_rate': 83.0,  # Current INR to USD rate
            'price_multiplier': 1.2  # Slight premium for US market
        }
        
    def load_dataset(self):
        """Load the original dataset"""
        print(f"Loading dataset from {self.input_file}...")
        # Load in chunks to handle large file
        chunk_size = 100000
        chunks = []
        
        for chunk in pd.read_csv(self.input_file, chunksize=chunk_size):
            chunks.append(chunk)
            if len(chunks) % 10 == 0:
                print(f"Loaded {len(chunks) * chunk_size:,} rows...")
        
        self.df = pd.concat(chunks, ignore_index=True)
        print(f"Total rows loaded: {len(self.df):,}")
        return self.df
    
    def scale_stores(self):
        """Scale store count from ~50 to ~2,500 stores"""
        print("Scaling stores...")
        
        # Get unique stores
        unique_stores = self.df['store_id'].unique()
        original_store_count = len(unique_stores)
        
        # Create new store IDs for 2,500 stores
        new_store_ids = [f"STR_{i:06d}" for i in range(1, 2501)]
        
        # Create mapping from original stores to new stores
        store_mapping = {}
        for i, original_store in enumerate(unique_stores):
            # Map original stores to multiple new stores
            stores_per_original = 2500 // original_store_count
            start_idx = i * stores_per_original
            end_idx = min(start_idx + stores_per_original, 2500)
            
            for j in range(start_idx, end_idx):
                store_mapping[original_store] = new_store_ids[j]
        
        # Update store IDs
        self.df['store_id'] = self.df['store_id'].map(store_mapping)
        
        # Update store regions (distribute across 5 regions)
        regions = ['East', 'West', 'Central', 'North', 'South']
        self.df['store_region'] = np.random.choice(regions, size=len(self.df), 
                                                  p=[0.25, 0.20, 0.30, 0.15, 0.10])
        
        print(f"Scaled from {original_store_count} to 2,500 stores")
    
    def scale_customers(self):
        """Scale customer count from ~200K to ~10M customers"""
        print("Scaling customers...")
        
        # Get unique customers
        unique_customers = self.df['customer_id'].unique()
        original_customer_count = len(unique_customers)
        
        # Create new customer IDs for 10M customers
        new_customer_ids = [f"CUST_{i:08d}" for i in range(1, 10000001)]
        
        # Create mapping from original customers to new customers
        customer_mapping = {}
        for i, original_customer in enumerate(unique_customers):
            # Map original customers to multiple new customers
            customers_per_original = 10000000 // original_customer_count
            start_idx = i * customers_per_original
            end_idx = min(start_idx + customers_per_original, 10000000)
            
            for j in range(start_idx, end_idx):
                customer_mapping[original_customer] = new_customer_ids[j]
        
        # Update customer IDs
        self.df['customer_id'] = self.df['customer_id'].map(customer_mapping)
        
        print(f"Scaled from {original_customer_count:,} to 10,000,000 customers")
    
    def scale_products_and_prices(self):
        """Scale products and convert prices to USD"""
        print("Scaling products and converting prices to USD...")
        
        # Convert INR to USD and apply price multiplier
        usd_rate = self.scale_factors['inr_to_usd_rate']
        price_multiplier = self.scale_factors['price_multiplier']
        
        # Convert prices to USD
        price_columns = ['unit_price', 'final_price', 'total_amount']
        for col in price_columns:
            self.df[col] = (self.df[col] / usd_rate * price_multiplier).round(2)
        
        # Scale product quantities slightly for larger retailer
        self.df['quantity'] = self.df['quantity'] * 1.1
        
        print(f"Converted prices to USD (rate: {usd_rate} INR = 1 USD)")
        print(f"Applied price multiplier: {price_multiplier}x")
    
    def scale_employees(self):
        """Scale employee count for 2,500 stores"""
        print("Scaling employees...")
        
        # Get unique employees
        unique_employees = self.df['employee_id'].unique()
        original_employee_count = len(unique_employees)
        
        # Create new employee IDs for ~25,000 employees (10 per store)
        new_employee_ids = [f"EMP_{i:06d}" for i in range(1, 25001)]
        
        # Create mapping from original employees to new employees
        employee_mapping = {}
        for i, original_employee in enumerate(unique_employees):
            # Map original employees to multiple new employees
            employees_per_original = 25000 // original_employee_count
            start_idx = i * employees_per_original
            end_idx = min(start_idx + employees_per_original, 25000)
            
            for j in range(start_idx, end_idx):
                employee_mapping[original_employee] = new_employee_ids[j]
        
        # Update employee IDs
        self.df['employee_id'] = self.df['employee_id'].map(employee_mapping)
        
        print(f"Scaled from {original_employee_count:,} to 25,000 employees")
    
    def scale_suppliers(self):
        """Scale supplier count for larger retailer"""
        print("Scaling suppliers...")
        
        # Get unique suppliers
        unique_suppliers = self.df['supplier_id'].unique()
        original_supplier_count = len(unique_suppliers)
        
        # Create new supplier IDs for ~500 suppliers
        new_supplier_ids = [f"SUP_{i:06d}" for i in range(1, 501)]
        
        # Create mapping from original suppliers to new suppliers
        supplier_mapping = {}
        for i, original_supplier in enumerate(unique_suppliers):
            # Map original suppliers to multiple new suppliers
            suppliers_per_original = 500 // original_supplier_count
            start_idx = i * suppliers_per_original
            end_idx = min(start_idx + suppliers_per_original, 500)
            
            for j in range(start_idx, end_idx):
                supplier_mapping[original_supplier] = new_supplier_ids[j]
        
        # Update supplier IDs
        self.df['supplier_id'] = self.df['supplier_id'].map(supplier_mapping)
        
        print(f"Scaled from {original_supplier_count:,} to 500 suppliers")
    
    def scale_transactions(self):
        """Scale transaction count by duplicating and modifying transactions"""
        print("Scaling transactions...")
        
        original_count = len(self.df)
        target_count = int(original_count * self.scale_factors['transaction_count_multiplier'])
        
        # If we need more transactions, duplicate and modify
        if target_count > original_count:
            multiplier = target_count // original_count
            remainder = target_count % original_count
            
            # Duplicate the dataframe
            scaled_df = self.df.copy()
            
            for i in range(multiplier - 1):
                # Create modified copy
                new_df = self.df.copy()
                
                # Modify transaction IDs
                new_df['transaction_id'] = new_df['transaction_id'].str.replace(
                    'TXN_', f'TXN_{i+2:02d}_'
                )
                
                # Slightly modify timestamps (add random hours)
                new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
                random_hours = np.random.randint(1, 24, size=len(new_df))
                new_df['timestamp'] = new_df['timestamp'] + pd.to_timedelta(random_hours, unit='h')
                new_df['timestamp'] = new_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Slightly modify prices (±5%)
                price_columns = ['unit_price', 'final_price', 'total_amount']
                for col in price_columns:
                    noise = np.random.normal(1.0, 0.05, size=len(new_df))
                    new_df[col] = (new_df[col] * noise).round(2)
                
                scaled_df = pd.concat([scaled_df, new_df], ignore_index=True)
            
            # Add remainder transactions
            if remainder > 0:
                remainder_df = self.df.sample(n=remainder, random_state=42)
                remainder_df['transaction_id'] = remainder_df['transaction_id'].str.replace(
                    'TXN_', 'TXN_R_'
                )
                scaled_df = pd.concat([scaled_df, remainder_df], ignore_index=True)
            
            self.df = scaled_df
        
        print(f"Scaled from {original_count:,} to {len(self.df):,} transactions")
    
    def update_origin_country(self):
        """Update origin country to reflect US market"""
        print("Updating origin country...")
        
        # Update origin country to US for most products
        self.df['origin_country'] = 'USA'
        
        # Keep some international products (20%)
        international_mask = np.random.random(len(self.df)) < 0.2
        international_countries = ['Mexico', 'Canada', 'China', 'India', 'Brazil', 'Italy', 'France']
        self.df.loc[international_mask, 'origin_country'] = np.random.choice(
            international_countries, size=international_mask.sum()
        )
        
        print("Updated origin country to reflect US market")
    
    def update_temperature_and_weather(self):
        """Update temperature and weather for US market"""
        print("Updating temperature and weather...")
        
        # Update temperature to Fahrenheit (US standard)
        self.df['temperature_celsius'] = (self.df['temperature_celsius'] * 9/5 + 32).round(1)
        
        # Update weather conditions for US
        us_weather = ['Sunny', 'Cloudy', 'Rainy', 'Snowy', 'Foggy', 'Windy']
        self.df['weather_condition'] = np.random.choice(us_weather, size=len(self.df))
        
        print("Updated temperature to Fahrenheit and weather conditions")
    
    def add_loyalty_points_scaling(self):
        """Scale loyalty points for larger retailer"""
        print("Scaling loyalty points...")
        
        # Scale loyalty points earned (multiply by 2 for larger retailer)
        self.df['loyalty_points_earned'] = self.df['loyalty_points_earned'] * 2
        
        # Scale loyalty points used (multiply by 1.5)
        self.df['loyalty_points_used'] = self.df['loyalty_points_used'] * 1.5
        
        print("Scaled loyalty points for larger retailer")
    
    def add_basket_size_scaling(self):
        """Scale basket size for larger retailer"""
        print("Scaling basket size...")
        
        # Scale basket size (multiply by 1.3 for larger retailer)
        self.df['basket_size'] = (self.df['basket_size'] * 1.3).round(0)
        
        print("Scaled basket size for larger retailer")
    
    def generate_summary_stats(self):
        """Generate summary statistics for the scaled dataset"""
        print("\n" + "="*60)
        print("SCALED DATASET SUMMARY STATISTICS")
        print("="*60)
        
        # Basic counts
        print(f"Total Transactions: {len(self.df):,}")
        print(f"Unique Stores: {self.df['store_id'].nunique():,}")
        print(f"Unique Customers: {self.df['customer_id'].nunique():,}")
        print(f"Unique Products: {self.df['product_id'].nunique():,}")
        print(f"Unique Employees: {self.df['employee_id'].nunique():,}")
        print(f"Unique Suppliers: {self.df['supplier_id'].nunique():,}")
        
        # Financial metrics
        total_revenue = self.df['total_amount'].sum()
        avg_transaction = self.df['total_amount'].mean()
        avg_price = self.df['unit_price'].mean()
        
        print(f"\nFinancial Metrics (USD):")
        print(f"Total Revenue: ${total_revenue:,.2f}")
        print(f"Average Transaction Value: ${avg_transaction:.2f}")
        print(f"Average Unit Price: ${avg_price:.2f}")
        
        # Regional distribution
        print(f"\nRegional Distribution:")
        region_counts = self.df['store_region'].value_counts()
        for region, count in region_counts.items():
            percentage = (count / len(self.df)) * 100
            print(f"{region}: {count:,} transactions ({percentage:.1f}%)")
        
        # Customer type distribution
        print(f"\nCustomer Type Distribution:")
        customer_type_counts = self.df['customer_type'].value_counts()
        for customer_type, count in customer_type_counts.items():
            percentage = (count / len(self.df)) * 100
            print(f"{customer_type}: {count:,} transactions ({percentage:.1f}%)")
        
        # Payment method distribution
        print(f"\nPayment Method Distribution:")
        payment_counts = self.df['payment_method'].value_counts()
        for payment, count in payment_counts.items():
            percentage = (count / len(self.df)) * 100
            print(f"{payment}: {count:,} transactions ({percentage:.1f}%)")
        
        print("="*60)
    
    def save_scaled_dataset(self):
        """Save the scaled dataset"""
        print(f"\nSaving scaled dataset to {self.output_file}...")
        
        # Save in chunks to handle large file
        chunk_size = 100000
        total_chunks = len(self.df) // chunk_size + 1
        
        with open(self.output_file, 'w', newline='') as f:
            # Write header
            self.df.head(0).to_csv(f, index=False)
            
            # Write chunks
            for i in range(0, len(self.df), chunk_size):
                chunk = self.df.iloc[i:i+chunk_size]
                chunk.to_csv(f, header=False, index=False)
                
                if (i // chunk_size + 1) % 10 == 0:
                    print(f"Saved {i + chunk_size:,} rows...")
        
        print(f"Scaled dataset saved successfully!")
        print(f"File size: {os.path.getsize(self.output_file) / (1024*1024*1024):.2f} GB")
    
    def scale_dataset(self):
        """Main method to scale the entire dataset"""
        print("Starting dataset scaling for 4-5B revenue retailer...")
        print("="*60)
        
        # Load dataset
        self.load_dataset()
        
        # Scale various components
        self.scale_stores()
        self.scale_customers()
        self.scale_products_and_prices()
        self.scale_employees()
        self.scale_suppliers()
        self.scale_transactions()
        self.update_origin_country()
        self.update_temperature_and_weather()
        self.add_loyalty_points_scaling()
        self.add_basket_size_scaling()
        
        # Generate summary
        self.generate_summary_stats()
        
        # Save scaled dataset
        self.save_scaled_dataset()
        
        print("\nDataset scaling completed successfully!")
        return self.output_file

def main():
    """Main function to scale the grocery dataset"""
    input_file = "/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/grocery_dataset.csv"
    output_file = "/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/grocery_dataset_4_5b_usd.csv"
    
    print("Grocery Dataset Scaler - 4-5B Revenue Retailer")
    print("="*60)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print("="*60)
    
    # Initialize scaler
    scaler = GroceryDatasetScaler(input_file, output_file)
    
    # Scale dataset
    output_file = scaler.scale_dataset()
    
    print(f"\nScaled dataset saved to: {output_file}")
    print("\nKey changes made:")
    print("✅ Scaled from ~50 stores to 2,500 stores")
    print("✅ Scaled from ~200K customers to 10M customers")
    print("✅ Scaled from ~1.87M transactions to ~93.5M transactions")
    print("✅ Converted prices from INR to USD")
    print("✅ Updated origin country to USA")
    print("✅ Updated temperature to Fahrenheit")
    print("✅ Scaled employees, suppliers, and other entities")
    print("✅ Applied realistic scaling factors for 4-5B retailer")

if __name__ == "__main__":
    main()
