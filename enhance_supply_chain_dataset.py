#!/usr/bin/env python3
"""
Enhanced Grocery Dataset Generator for Supply Chain Analysis
Adds fields for demand forecasting, replenishment, clustering, assortment, pricing, promotion, space planning, planogram
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

class SupplyChainDatasetEnhancer:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.backup_file = input_file.replace('.csv', '_supply_chain_backup.csv')
        
    def enhance_dataset(self):
        print("============================================================")
        print("Enhancing dataset for Supply Chain Analysis...")
        print("============================================================")

        # Create backup
        print(f"Creating backup: {self.backup_file}")
        pd.read_csv(self.input_file).to_csv(self.backup_file, index=False)
        print("Backup created successfully!")

        print(f"Loading dataset from {self.input_file}...")
        df = pd.read_csv(self.input_file)
        print(f"Total rows loaded: {len(df)}")

        # Add demand forecasting fields
        print("Adding demand forecasting fields...")
        df = self._add_demand_forecasting_fields(df)
        
        # Add replenishment fields
        print("Adding replenishment fields...")
        df = self._add_replenishment_fields(df)
        
        # Add clustering and assortment fields
        print("Adding clustering and assortment fields...")
        df = self._add_clustering_assortment_fields(df)
        
        # Add pricing and promotion fields
        print("Adding pricing and promotion fields...")
        df = self._add_pricing_promotion_fields(df)
        
        # Add space planning and planogram fields
        print("Adding space planning and planogram fields...")
        df = self._add_space_planning_fields(df)
        
        # Add supplier performance fields
        print("Adding supplier performance fields...")
        df = self._add_supplier_performance_fields(df)

        print("\n============================================================")
        print("ENHANCED DATASET SUMMARY")
        print("============================================================")
        print(f"Total Rows: {len(df):,}")
        print(f"Total Columns: {len(df.columns)}")
        print("\nNew Supply Chain Fields Added:")
        
        # List new fields
        new_fields = [
            'forecast_accuracy', 'demand_volatility', 'weather_impact_score',
            'replenishment_lead_time', 'safety_stock_level', 'reorder_point',
            'store_cluster', 'assortment_efficiency', 'sku_performance_score',
            'price_elasticity', 'promotional_lift', 'margin_impact',
            'space_utilization', 'planogram_efficiency', 'customer_flow_score',
            'supplier_performance_score', 'delivery_reliability', 'quality_score'
        ]
        
        for field in new_fields:
            if field in df.columns:
                print(f"✅ {field}")
        
        print(f"\nSaving enhanced dataset to {self.input_file}...")
        df.to_csv(self.input_file, index=False)
        print("Enhanced dataset saved successfully!")
        print(f"File size: {os.path.getsize(self.input_file) / (1024*1024):.2f} MB")

        return df

    def _add_demand_forecasting_fields(self, df):
        """Add demand forecasting related fields"""
        # Forecast accuracy (0-100%)
        df['forecast_accuracy'] = np.random.normal(78, 15, len(df))
        df['forecast_accuracy'] = df['forecast_accuracy'].clip(50, 95)
        
        # Demand volatility (coefficient of variation)
        df['demand_volatility'] = np.random.exponential(0.3, len(df))
        df['demand_volatility'] = df['demand_volatility'].clip(0.1, 1.0)
        
        # Weather impact score (0-100)
        weather_conditions = df['weather_condition'].map({
            'Sunny': 20, 'Cloudy': 40, 'Rainy': 80, 'Stormy': 95
        }).fillna(50)
        df['weather_impact_score'] = weather_conditions + np.random.normal(0, 10, len(df))
        df['weather_impact_score'] = df['weather_impact_score'].clip(0, 100)
        
        # Seasonal demand factor
        df['seasonal_demand_factor'] = df['season'].map({
            'Spring': 1.1, 'Summer': 1.3, 'Fall': 0.9, 'Winter': 0.8
        }).fillna(1.0)
        
        return df

    def _add_replenishment_fields(self, df):
        """Add replenishment related fields"""
        # Replenishment lead time (days)
        df['replenishment_lead_time'] = np.random.choice([1, 2, 3, 5, 7, 14], 
                                                       len(df), p=[0.1, 0.2, 0.3, 0.25, 0.1, 0.05])
        
        # Safety stock level (units)
        df['safety_stock_level'] = (df['quantity'] * np.random.uniform(0.2, 0.8, len(df))).astype(int)
        
        # Reorder point (units)
        df['reorder_point'] = (df['quantity'] * np.random.uniform(0.5, 1.5, len(df))).astype(int)
        
        # Inventory turnover by category
        category_turns = {
            'Fresh Produce': 2.1, 'Beverages': 4.8, 'Snacks': 6.2, 
            'Dairy': 3.5, 'Meat': 2.8, 'Household Items': 4.2,
            'Cooking Essentials': 3.8, 'Frozen Foods': 3.2
        }
        df['inventory_turnover'] = df['category'].map(category_turns).fillna(4.0)
        
        # Stockout risk score (0-100)
        df['stockout_risk_score'] = np.random.beta(2, 5, len(df)) * 100
        
        return df

    def _add_clustering_assortment_fields(self, df):
        """Add clustering and assortment related fields"""
        # Store cluster (based on performance)
        df['store_cluster'] = df['store_region'].map({
            'East': 'High Performance', 'West': 'Low Performance', 
            'Central': 'Medium Performance', 'North': 'Medium Performance', 
            'South': 'Low Performance'
        })
        
        # Assortment efficiency (0-100%)
        df['assortment_efficiency'] = np.random.normal(65, 15, len(df))
        df['assortment_efficiency'] = df['assortment_efficiency'].clip(30, 95)
        
        # SKU performance score (0-100)
        df['sku_performance_score'] = np.random.beta(3, 2, len(df)) * 100
        
        # Category importance score (0-100)
        category_importance = {
            'Fresh Produce': 90, 'Beverages': 85, 'Snacks': 70, 
            'Dairy': 80, 'Meat': 85, 'Household Items': 60,
            'Cooking Essentials': 75, 'Frozen Foods': 70
        }
        df['category_importance_score'] = df['category'].map(category_importance).fillna(70)
        
        # Local market penetration (0-100%)
        df['local_market_penetration'] = np.random.normal(75, 20, len(df))
        df['local_market_penetration'] = df['local_market_penetration'].clip(20, 100)
        
        return df

    def _add_pricing_promotion_fields(self, df):
        """Add pricing and promotion related fields"""
        # Price elasticity (negative values)
        df['price_elasticity'] = -np.random.exponential(1.5, len(df))
        df['price_elasticity'] = df['price_elasticity'].clip(-5.0, -0.5)
        
        # Promotional lift (percentage)
        df['promotional_lift'] = np.random.exponential(15, len(df))
        df['promotional_lift'] = df['promotional_lift'].clip(5, 50)
        
        # Margin impact (percentage points)
        df['margin_impact'] = np.random.normal(-5, 8, len(df))
        df['margin_impact'] = df['margin_impact'].clip(-20, 10)
        
        # Competitive price position (0-100%)
        df['competitive_price_position'] = np.random.normal(75, 15, len(df))
        df['competitive_price_position'] = df['competitive_price_position'].clip(30, 100)
        
        # Price sensitivity score (0-100)
        df['price_sensitivity_score'] = np.random.beta(3, 2, len(df)) * 100
        
        # Promotion effectiveness (0-100%)
        df['promotion_effectiveness'] = np.random.normal(60, 20, len(df))
        df['promotion_effectiveness'] = df['promotion_effectiveness'].clip(20, 95)
        
        return df

    def _add_space_planning_fields(self, df):
        """Add space planning and planogram related fields"""
        # Space utilization (0-100%)
        df['space_utilization'] = np.random.normal(78, 15, len(df))
        df['space_utilization'] = df['space_utilization'].clip(40, 100)
        
        # Planogram efficiency (0-100%)
        df['planogram_efficiency'] = np.random.normal(72, 18, len(df))
        df['planogram_efficiency'] = df['planogram_efficiency'].clip(30, 95)
        
        # Customer flow score (0-100)
        df['customer_flow_score'] = np.random.normal(75, 20, len(df))
        df['customer_flow_score'] = df['customer_flow_score'].clip(30, 100)
        
        # Sales per square foot
        df['sales_per_sqft'] = np.random.normal(900, 200, len(df))
        df['sales_per_sqft'] = df['sales_per_sqft'].clip(400, 1500)
        
        # Visual merchandising score (0-100)
        df['visual_merchandising_score'] = np.random.normal(70, 20, len(df))
        df['visual_merchandising_score'] = df['visual_merchandising_score'].clip(20, 95)
        
        # Category space allocation (percentage)
        df['category_space_allocation'] = np.random.uniform(5, 25, len(df))
        
        return df

    def _add_supplier_performance_fields(self, df):
        """Add supplier performance related fields"""
        # Supplier performance score (0-100)
        df['supplier_performance_score'] = np.random.normal(72, 20, len(df))
        df['supplier_performance_score'] = df['supplier_performance_score'].clip(30, 100)
        
        # Delivery reliability (0-100%)
        df['delivery_reliability'] = np.random.normal(75, 15, len(df))
        df['delivery_reliability'] = df['delivery_reliability'].clip(40, 100)
        
        # Quality score (0-100)
        df['quality_score'] = np.random.normal(80, 15, len(df))
        df['quality_score'] = df['quality_score'].clip(50, 100)
        
        # Supplier cost efficiency (0-100%)
        df['supplier_cost_efficiency'] = np.random.normal(70, 20, len(df))
        df['supplier_cost_efficiency'] = df['supplier_cost_efficiency'].clip(30, 100)
        
        # Supplier innovation score (0-100%)
        df['supplier_innovation_score'] = np.random.normal(65, 20, len(df))
        df['supplier_innovation_score'] = df['supplier_innovation_score'].clip(20, 95)
        
        # Supplier risk score (0-100)
        df['supplier_risk_score'] = np.random.beta(2, 5, len(df)) * 100
        
        return df

def main():
    """Main function to enhance the dataset for supply chain analysis"""
    print("Supply Chain Dataset Enhancer")
    print("=" * 60)
    
    input_csv_path = "/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/grocery_dataset.csv"
    enhancer = SupplyChainDatasetEnhancer(input_csv_path)
    
    enhanced_df = enhancer.enhance_dataset()
    
    print("\nDataset Enhancement Complete!")
    print(f"Enhanced dataset saved to: {input_csv_path}")
    print("\nNew fields added for:")
    print("✅ Demand Forecasting & Planning")
    print("✅ Inventory Management & Replenishment")
    print("✅ Store Clustering & Assortment Optimization")
    print("✅ Pricing & Promotion Optimization")
    print("✅ Space Planning & Planogram Management")
    print("✅ Supplier Relationship & Performance Management")

if __name__ == "__main__":
    main()
