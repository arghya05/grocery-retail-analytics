#!/usr/bin/env python3
"""
Fundamental Merchandising Strategy Analysis
Analyzes the dataset to identify core merchandising challenges that leaders actually ask
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

def analyze_merchandising_strategy():
    """Analyze fundamental merchandising strategy questions"""
    print("Loading dataset for merchandising analysis...")
    df = pd.read_csv("/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/grocery_dataset.csv")
    print(f"Loaded {len(df):,} transactions")
    
    insights = {}
    
    # 1. Category Strategy Analysis
    print("Analyzing category strategy...")
    category_analysis = df.groupby('category').agg({
        'total_amount': ['sum', 'mean', 'count'],
        'unit_price': 'mean',
        'margin_impact': 'mean',
        'inventory_turnover': 'mean',
        'price_elasticity': 'mean',
        'promotional_lift': 'mean',
        'sales_per_sqft': 'mean'
    }).round(2)
    
    # Top revenue categories
    top_revenue = df.groupby('category')['total_amount'].sum().sort_values(ascending=False).head(5)
    # Lowest margin categories
    lowest_margin = df.groupby('category')['margin_impact'].mean().sort_values().head(5)
    # Slowest turning categories
    slowest_turnover = df.groupby('category')['inventory_turnover'].mean().sort_values().head(5)
    
    insights['category_strategy'] = {
        'top_revenue_categories': top_revenue.to_dict(),
        'lowest_margin_categories': lowest_margin.to_dict(),
        'slowest_turnover_categories': slowest_turnover.to_dict()
    }
    
    # 2. Brand Strategy Analysis
    print("Analyzing brand strategy...")
    brand_revenue = df.groupby('brand')['total_amount'].sum().sort_values(ascending=False).head(10)
    brand_margin = df.groupby('brand')['margin_impact'].mean().sort_values().head(10)
    
    insights['brand_strategy'] = {
        'top_revenue_brands': brand_revenue.to_dict(),
        'lowest_margin_brands': brand_margin.to_dict()
    }
    
    # 3. Price Strategy Analysis
    print("Analyzing price strategy...")
    price_elasticity = df.groupby('category')['price_elasticity'].mean().sort_values().head(5)
    price_sensitivity = df.groupby('category')['price_sensitivity_score'].mean().sort_values(ascending=False).head(5)
    
    insights['price_strategy'] = {
        'most_elastic_categories': price_elasticity.to_dict(),
        'most_sensitive_categories': price_sensitivity.to_dict()
    }
    
    # 4. Promotional Strategy Analysis
    print("Analyzing promotional strategy...")
    promo_lift = df.groupby('category')['promotional_lift'].mean().sort_values(ascending=False).head(5)
    promo_effectiveness = df.groupby('category')['promotion_effectiveness'].mean().sort_values(ascending=False).head(5)
    
    insights['promotional_strategy'] = {
        'highest_lift_categories': promo_lift.to_dict(),
        'most_effective_categories': promo_effectiveness.to_dict()
    }
    
    # 5. Space Strategy Analysis
    print("Analyzing space strategy...")
    sales_density = df.groupby('category')['sales_per_sqft'].mean().sort_values(ascending=False).head(5)
    space_allocation = df.groupby('category')['category_space_allocation'].mean().sort_values(ascending=False).head(5)
    
    insights['space_strategy'] = {
        'highest_density_categories': sales_density.to_dict(),
        'highest_allocation_categories': space_allocation.to_dict()
    }
    
    # 6. Customer Strategy Analysis
    print("Analyzing customer strategy...")
    customer_value = df.groupby('customer_type')['total_amount'].sum().sort_values(ascending=False)
    customer_basket = df.groupby('customer_type')['basket_size'].mean().sort_values(ascending=False)
    
    insights['customer_strategy'] = {
        'customer_value_by_type': customer_value.to_dict(),
        'customer_basket_by_type': customer_basket.to_dict()
    }
    
    # 7. Critical Challenges
    print("Identifying critical challenges...")
    negative_margin_items = len(df[df['margin_impact'] < -10])
    high_elasticity_items = len(df[df['price_elasticity'] < -3.0])
    ineffective_promotions = len(df[df['promotional_lift'] < 10])
    underutilized_space = len(df[df['space_utilization'] < 70])
    low_performing_skus = len(df[df['sku_performance_score'] < 50])
    
    insights['critical_challenges'] = {
        'negative_margin_items': negative_margin_items,
        'high_elasticity_items': high_elasticity_items,
        'ineffective_promotions': ineffective_promotions,
        'underutilized_space': underutilized_space,
        'low_performing_skus': low_performing_skus,
        'total_transactions': len(df)
    }
    
    # Save insights
    output_path = "/Users/arghya.mukherjee/Downloads/cursor/sd/supply_chain/merchandising_strategy_insights.json"
    with open(output_path, 'w') as f:
        json.dump(insights, f, indent=2)
    
    print(f"Merchandising insights saved to {output_path}")
    return insights

if __name__ == "__main__":
    insights = analyze_merchandising_strategy()
    
    print("\n" + "="*70)
    print("FUNDAMENTAL MERCHANDISING STRATEGY INSIGHTS")
    print("="*70)
    
    print("\nTOP REVENUE CATEGORIES:")
    for category, revenue in list(insights['category_strategy']['top_revenue_categories'].items())[:3]:
        print(f"  {category}: ${revenue:,.0f}")
    
    print("\nLOWEST MARGIN CATEGORIES:")
    for category, margin in list(insights['category_strategy']['lowest_margin_categories'].items())[:3]:
        print(f"  {category}: {margin:.1f}%")
    
    print("\nMOST PRICE-ELASTIC CATEGORIES:")
    for category, elasticity in list(insights['price_strategy']['most_elastic_categories'].items())[:3]:
        print(f"  {category}: {elasticity:.2f}")
    
    print("\nCRITICAL CHALLENGES:")
    print(f"  Negative Margin Items: {insights['critical_challenges']['negative_margin_items']:,}")
    print(f"  High Elasticity Items: {insights['critical_challenges']['high_elasticity_items']:,}")
    print(f"  Ineffective Promotions: {insights['critical_challenges']['ineffective_promotions']:,}")
    print(f"  Underutilized Space: {insights['critical_challenges']['underutilized_space']:,}")
    print(f"  Low Performing SKUs: {insights['critical_challenges']['low_performing_skus']:,}")