#!/usr/bin/env python3
"""
Comprehensive Supply Chain Operations Analysis
Analyzes both merchandising strategy and operational health metrics
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

def analyze_comprehensive_supply_chain():
    """Analyze both merchandising strategy and operational health"""
    print("Loading dataset for comprehensive supply chain analysis...")
    df = pd.read_csv("/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/grocery_dataset.csv")
    print(f"Loaded {len(df):,} transactions")
    
    insights = {}
    
    # ===== MERCHANDISING STRATEGY ANALYSIS =====
    print("Analyzing merchandising strategy...")
    
    # Category Strategy
    category_revenue = df.groupby('category')['total_amount'].sum().sort_values(ascending=False).head(5)
    category_margin = df.groupby('category')['margin_impact'].mean().sort_values().head(5)
    category_turnover = df.groupby('category')['inventory_turnover'].mean().sort_values().head(5)
    
    # Brand Strategy
    brand_revenue = df.groupby('brand')['total_amount'].sum().sort_values(ascending=False).head(10)
    brand_margin = df.groupby('brand')['margin_impact'].mean().sort_values().head(10)
    
    # Pricing Strategy
    price_elasticity = df.groupby('category')['price_elasticity'].mean().sort_values().head(5)
    price_sensitivity = df.groupby('category')['price_sensitivity_score'].mean().sort_values(ascending=False).head(5)
    
    # Promotional Strategy
    promo_lift = df.groupby('category')['promotional_lift'].mean().sort_values(ascending=False).head(5)
    promo_effectiveness = df.groupby('category')['promotion_effectiveness'].mean().sort_values(ascending=False).head(5)
    
    # Space Strategy
    sales_density = df.groupby('category')['sales_per_sqft'].mean().sort_values(ascending=False).head(5)
    space_allocation = df.groupby('category')['category_space_allocation'].mean().sort_values(ascending=False).head(5)
    
    # Customer Strategy
    customer_value = df.groupby('customer_type')['total_amount'].sum().sort_values(ascending=False)
    customer_basket = df.groupby('customer_type')['basket_size'].mean().sort_values(ascending=False)
    
    insights['merchandising_strategy'] = {
        'category_strategy': {
            'top_revenue_categories': category_revenue.to_dict(),
            'lowest_margin_categories': category_margin.to_dict(),
            'slowest_turnover_categories': category_turnover.to_dict()
        },
        'brand_strategy': {
            'top_revenue_brands': brand_revenue.to_dict(),
            'lowest_margin_brands': brand_margin.to_dict()
        },
        'price_strategy': {
            'most_elastic_categories': price_elasticity.to_dict(),
            'most_sensitive_categories': price_sensitivity.to_dict()
        },
        'promotional_strategy': {
            'highest_lift_categories': promo_lift.to_dict(),
            'most_effective_categories': promo_effectiveness.to_dict()
        },
        'space_strategy': {
            'highest_density_categories': sales_density.to_dict(),
            'highest_allocation_categories': space_allocation.to_dict()
        },
        'customer_strategy': {
            'customer_value_by_type': customer_value.to_dict(),
            'customer_basket_by_type': customer_basket.to_dict()
        }
    }
    
    # ===== OPERATIONAL HEALTH ANALYSIS =====
    print("Analyzing operational health...")
    
    # Inventory Management
    inventory_turnover = df.groupby('category')['inventory_turnover'].mean().sort_values()
    stockout_risk = df.groupby('category')['stockout_risk_score'].mean().sort_values(ascending=False)
    safety_stock = df.groupby('category')['safety_stock_level'].mean().sort_values(ascending=False)
    
    # Forecast Accuracy
    forecast_accuracy = df.groupby('category')['forecast_accuracy'].mean().sort_values(ascending=False)
    demand_volatility = df.groupby('category')['demand_volatility'].mean().sort_values(ascending=False)
    
    # Supplier Performance
    supplier_performance = df.groupby('supplier_id')['supplier_performance_score'].mean().sort_values(ascending=False).head(20)
    delivery_reliability = df.groupby('supplier_id')['delivery_reliability'].mean().sort_values(ascending=False).head(20)
    supplier_cost_efficiency = df.groupby('supplier_id')['supplier_cost_efficiency'].mean().sort_values(ascending=False).head(20)
    
    # Lead Time Analysis
    lead_time = df.groupby('category')['replenishment_lead_time'].mean().sort_values(ascending=False)
    
    # Store Operations
    store_performance = df.groupby('store_type')['sales_per_sqft'].mean().sort_values(ascending=False)
    space_utilization = df.groupby('store_type')['space_utilization'].mean().sort_values(ascending=False)
    
    insights['operational_health'] = {
        'inventory_management': {
            'slowest_turnover_categories': inventory_turnover.head(5).to_dict(),
            'highest_stockout_risk': stockout_risk.head(5).to_dict(),
            'highest_safety_stock': safety_stock.head(5).to_dict()
        },
        'forecast_accuracy': {
            'lowest_accuracy_categories': forecast_accuracy.tail(5).to_dict(),
            'highest_volatility_categories': demand_volatility.head(5).to_dict()
        },
        'supplier_performance': {
            'top_performing_suppliers': supplier_performance.head(10).to_dict(),
            'most_reliable_deliveries': delivery_reliability.head(10).to_dict(),
            'most_cost_efficient': supplier_cost_efficiency.head(10).to_dict()
        },
        'lead_time_analysis': {
            'longest_lead_times': lead_time.head(5).to_dict()
        },
        'store_operations': {
            'store_type_performance': store_performance.to_dict(),
            'space_utilization_by_type': space_utilization.to_dict()
        }
    }
    
    # ===== CRITICAL CHALLENGES =====
    print("Identifying critical challenges...")
    
    # Merchandising Challenges
    negative_margin_items = len(df[df['margin_impact'] < -10])
    high_elasticity_items = len(df[df['price_elasticity'] < -3.0])
    ineffective_promotions = len(df[df['promotional_lift'] < 10])
    underutilized_space = len(df[df['space_utilization'] < 70])
    low_performing_skus = len(df[df['sku_performance_score'] < 50])
    
    # Operational Challenges
    low_turnover_items = len(df[df['inventory_turnover'] < 2.0])
    high_stockout_risk = len(df[df['stockout_risk_score'] > 70])
    poor_forecast_accuracy = len(df[df['forecast_accuracy'] < 70])
    unreliable_suppliers = len(df[df['supplier_performance_score'] < 60])
    long_lead_times = len(df[df['replenishment_lead_time'] > 7])
    
    insights['critical_challenges'] = {
        'merchandising_challenges': {
            'negative_margin_items': negative_margin_items,
            'high_elasticity_items': high_elasticity_items,
            'ineffective_promotions': ineffective_promotions,
            'underutilized_space': underutilized_space,
            'low_performing_skus': low_performing_skus
        },
        'operational_challenges': {
            'low_turnover_items': low_turnover_items,
            'high_stockout_risk': high_stockout_risk,
            'poor_forecast_accuracy': poor_forecast_accuracy,
            'unreliable_suppliers': unreliable_suppliers,
            'long_lead_times': long_lead_times
        },
        'total_transactions': len(df)
    }
    
    # Save insights
    output_path = "/Users/arghya.mukherjee/Downloads/cursor/sd/supply_chain/comprehensive_supply_chain_insights.json"
    with open(output_path, 'w') as f:
        json.dump(insights, f, indent=2)
    
    print(f"Comprehensive insights saved to {output_path}")
    return insights

if __name__ == "__main__":
    insights = analyze_comprehensive_supply_chain()
    
    print("\n" + "="*80)
    print("COMPREHENSIVE SUPPLY CHAIN OPERATIONS INSIGHTS")
    print("="*80)
    
    print("\nMERCHANDISING STRATEGY:")
    print("Top Revenue Categories:")
    for category, revenue in list(insights['merchandising_strategy']['category_strategy']['top_revenue_categories'].items())[:3]:
        print(f"  {category}: ${revenue:,.0f}")
    
    print("\nOPERATIONAL HEALTH:")
    print("Slowest Turnover Categories:")
    for category, turnover in list(insights['operational_health']['inventory_management']['slowest_turnover_categories'].items())[:3]:
        print(f"  {category}: {turnover:.1f}x")
    
    print("\nCRITICAL CHALLENGES:")
    print(f"  Merchandising: {insights['critical_challenges']['merchandising_challenges']['negative_margin_items']:,} negative margin items")
    print(f"  Operational: {insights['critical_challenges']['operational_challenges']['low_turnover_items']:,} low turnover items")
    print(f"  Forecast: {insights['critical_challenges']['operational_challenges']['poor_forecast_accuracy']:,} poor forecast accuracy")
    print(f"  Suppliers: {insights['critical_challenges']['operational_challenges']['unreliable_suppliers']:,} unreliable suppliers")
