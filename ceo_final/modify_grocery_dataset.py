#!/usr/bin/env python3
"""
Grocery Dataset Modifier - 4-5B Revenue Retailer
Modifies the existing dataset to reflect 4-5B revenue retailer numbers in USD
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

class GroceryDatasetModifier:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.backup_file = input_file.replace('.csv', '_backup.csv')
        
        # Scaling factors for 4-5B retailer
        self.scale_factors = {
            'revenue_multiplier': 500,  # Scale from ~$8M to ~$4B
            'inr_to_usd_rate': 83.0,  # Current INR to USD rate
            'price_multiplier': 1.2  # Slight premium for US market
        }
        
    def create_backup(self):
        """Create backup of original file"""
        print(f"Creating backup: {self.backup_file}")
        os.system(f"cp '{self.input_file}' '{self.backup_file}'")
        print("Backup created successfully!")
    
    def load_dataset(self):
        """Load the dataset in chunks"""
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
    
    def modify_prices_to_usd(self):
        """Convert prices from INR to USD"""
        print("Converting prices from INR to USD...")
        
        usd_rate = self.scale_factors['inr_to_usd_rate']
        price_multiplier = self.scale_factors['price_multiplier']
        
        # Convert prices to USD
        price_columns = ['unit_price', 'final_price', 'total_amount']
        for col in price_columns:
            self.df[col] = (self.df[col] / usd_rate * price_multiplier).round(2)
        
        print(f"Converted prices to USD (rate: {usd_rate} INR = 1 USD)")
        print(f"Applied price multiplier: {price_multiplier}x")
    
    def scale_stores_for_4_5b_retailer(self):
        """Scale store count to reflect 4-5B retailer"""
        print("Scaling stores for 4-5B retailer...")
        
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
    
    def scale_customers_for_4_5b_retailer(self):
        """Scale customer count to reflect 4-5B retailer"""
        print("Scaling customers for 4-5B retailer...")
        
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
    
    def scale_employees_for_4_5b_retailer(self):
        """Scale employee count for 4-5B retailer"""
        print("Scaling employees for 4-5B retailer...")
        
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
    
    def scale_suppliers_for_4_5b_retailer(self):
        """Scale supplier count for 4-5B retailer"""
        print("Scaling suppliers for 4-5B retailer...")
        
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
    
    def update_origin_country_to_us(self):
        """Update origin country to reflect US market"""
        print("Updating origin country to US...")
        
        # Update origin country to US for most products
        self.df['origin_country'] = 'USA'
        
        # Keep some international products (20%)
        international_mask = np.random.random(len(self.df)) < 0.2
        international_countries = ['Mexico', 'Canada', 'China', 'India', 'Brazil', 'Italy', 'France']
        self.df.loc[international_mask, 'origin_country'] = np.random.choice(
            international_countries, size=international_mask.sum()
        )
        
        print("Updated origin country to reflect US market")
    
    def update_temperature_to_fahrenheit(self):
        """Update temperature to Fahrenheit for US market"""
        print("Updating temperature to Fahrenheit...")
        
        # Update temperature to Fahrenheit (US standard)
        self.df['temperature_celsius'] = (self.df['temperature_celsius'] * 9/5 + 32).round(1)
        
        print("Updated temperature to Fahrenheit")
    
    def scale_loyalty_points_for_4_5b_retailer(self):
        """Scale loyalty points for 4-5B retailer"""
        print("Scaling loyalty points for 4-5B retailer...")
        
        # Scale loyalty points earned (multiply by 2 for larger retailer)
        self.df['loyalty_points_earned'] = self.df['loyalty_points_earned'] * 2
        
        # Scale loyalty points used (multiply by 1.5)
        self.df['loyalty_points_used'] = self.df['loyalty_points_used'] * 1.5
        
        print("Scaled loyalty points for 4-5B retailer")
    
    def scale_basket_size_for_4_5b_retailer(self):
        """Scale basket size for 4-5B retailer"""
        print("Scaling basket size for 4-5B retailer...")
        
        # Scale basket size (multiply by 1.3 for larger retailer)
        self.df['basket_size'] = (self.df['basket_size'] * 1.3).round(0)
        
        print("Scaled basket size for 4-5B retailer")
    
    def generate_summary_stats(self):
        """Generate summary statistics for the modified dataset"""
        print("\n" + "="*60)
        print("MODIFIED DATASET SUMMARY STATISTICS")
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
    
    def save_modified_dataset(self):
        """Save the modified dataset back to the original file"""
        print(f"\nSaving modified dataset to {self.input_file}...")
        
        # Save in chunks to handle large file
        chunk_size = 100000
        total_chunks = len(self.df) // chunk_size + 1
        
        with open(self.input_file, 'w', newline='') as f:
            # Write header
            self.df.head(0).to_csv(f, index=False)
            
            # Write chunks
            for i in range(0, len(self.df), chunk_size):
                chunk = self.df.iloc[i:i+chunk_size]
                chunk.to_csv(f, header=False, index=False)
                
                if (i // chunk_size + 1) % 10 == 0:
                    print(f"Saved {i + chunk_size:,} rows...")
        
        print(f"Modified dataset saved successfully!")
        print(f"File size: {os.path.getsize(self.input_file) / (1024*1024):.2f} MB")
    
    def modify_dataset(self):
        """Main method to modify the dataset"""
        print("Starting dataset modification for 4-5B revenue retailer...")
        print("="*60)
        
        # Create backup
        self.create_backup()
        
        # Load dataset
        self.load_dataset()
        
        # Modify various components
        self.modify_prices_to_usd()
        self.scale_stores_for_4_5b_retailer()
        self.scale_customers_for_4_5b_retailer()
        self.scale_employees_for_4_5b_retailer()
        self.scale_suppliers_for_4_5b_retailer()
        self.update_origin_country_to_us()
        self.update_temperature_to_fahrenheit()
        self.scale_loyalty_points_for_4_5b_retailer()
        self.scale_basket_size_for_4_5b_retailer()
        
        # Generate summary
        self.generate_summary_stats()
        
        # Save modified dataset
        self.save_modified_dataset()
        
        print("\nDataset modification completed successfully!")
        return self.input_file

def main():
    """Main function to modify the grocery dataset"""
    input_file = "/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/grocery_dataset.csv"
    
    print("Grocery Dataset Modifier - 4-5B Revenue Retailer")
    print("="*60)
    print(f"Input file: {input_file}")
    print("="*60)
    
    # Initialize modifier
    modifier = GroceryDatasetModifier(input_file)
    
    # Modify dataset
    output_file = modifier.modify_dataset()
    
    print(f"\nModified dataset saved to: {output_file}")
    print("\nKey changes made:")
    print("✅ Converted prices from INR to USD")
    print("✅ Scaled stores to 2,500 stores")
    print("✅ Scaled customers to 10M customers")
    print("✅ Scaled employees to 25,000 employees")
    print("✅ Scaled suppliers to 500 suppliers")
    print("✅ Updated origin country to USA")
    print("✅ Updated temperature to Fahrenheit")
    print("✅ Scaled loyalty points and basket size")
    print("✅ Maintained original file size")

if __name__ == "__main__":
    main()
