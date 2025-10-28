#!/usr/bin/env python3
"""
Industry Benchmark Analysis for Supply Chain Operations
Analyzes our performance against industry benchmarks
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

def analyze_industry_benchmarks():
    """Analyze our performance against industry benchmarks"""
    print("Loading dataset for industry benchmark analysis...")
    df = pd.read_csv("/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/grocery_dataset.csv")
    print(f"Loaded {len(df):,} transactions")
    
    benchmarks = {}
    
    # ===== CATEGORY PERFORMANCE BENCHMARKS =====
    print("Analyzing category performance benchmarks...")
    
    # Our actual performance
    category_revenue = df.groupby('category')['total_amount'].sum().sort_values(ascending=False)
    category_margin = df.groupby('category')['margin_impact'].mean()
    category_turnover = df.groupby('category')['inventory_turnover'].mean()
    
    # Industry benchmarks (typical grocery retail)
    industry_benchmarks = {
        'category_performance': {
            'Beverages': {
                'our_revenue': category_revenue.get('Beverages', 0),
                'our_margin': category_margin.get('Beverages', 0),
                'our_turnover': category_turnover.get('Beverages', 0),
                'industry_margin': 8.0,  # Industry benchmark
                'industry_turnover': 6.0,  # Industry benchmark
                'gap_margin': category_margin.get('Beverages', 0) - 8.0,
                'gap_turnover': category_turnover.get('Beverages', 0) - 6.0
            },
            'Fresh Produce': {
                'our_revenue': category_revenue.get('Fresh Produce', 0),
                'our_margin': category_margin.get('Fresh Produce', 0),
                'our_turnover': category_turnover.get('Fresh Produce', 0),
                'industry_margin': 12.0,  # Industry benchmark
                'industry_turnover': 4.5,  # Industry benchmark
                'gap_margin': category_margin.get('Fresh Produce', 0) - 12.0,
                'gap_turnover': category_turnover.get('Fresh Produce', 0) - 4.5
            },
            'Staples & Grains': {
                'our_revenue': category_revenue.get('Staples & Grains', 0),
                'our_margin': category_margin.get('Staples & Grains', 0),
                'our_turnover': category_turnover.get('Staples & Grains', 0),
                'industry_margin': 6.0,  # Industry benchmark
                'industry_turnover': 5.5,  # Industry benchmark
                'gap_margin': category_margin.get('Staples & Grains', 0) - 6.0,
                'gap_turnover': category_turnover.get('Staples & Grains', 0) - 5.5
            }
        }
    }
    
    # ===== OPERATIONAL BENCHMARKS =====
    print("Analyzing operational benchmarks...")
    
    # Forecast accuracy benchmarks
    forecast_accuracy = df['forecast_accuracy'].mean()
    industry_forecast_benchmark = 85.0  # Industry benchmark
    
    # Inventory turnover benchmarks
    avg_turnover = df['inventory_turnover'].mean()
    industry_turnover_benchmark = 5.2  # Industry benchmark
    
    # Space utilization benchmarks
    space_utilization = df['space_utilization'].mean()
    industry_space_benchmark = 85.0  # Industry benchmark
    
    # Supplier performance benchmarks
    supplier_performance = df['supplier_performance_score'].mean()
    industry_supplier_benchmark = 88.0  # Industry benchmark
    
    operational_benchmarks = {
        'forecast_accuracy': {
            'our_performance': forecast_accuracy,
            'industry_benchmark': industry_forecast_benchmark,
            'gap': forecast_accuracy - industry_forecast_benchmark,
            'performance_vs_benchmark': (forecast_accuracy / industry_forecast_benchmark) * 100
        },
        'inventory_turnover': {
            'our_performance': avg_turnover,
            'industry_benchmark': industry_turnover_benchmark,
            'gap': avg_turnover - industry_turnover_benchmark,
            'performance_vs_benchmark': (avg_turnover / industry_turnover_benchmark) * 100
        },
        'space_utilization': {
            'our_performance': space_utilization,
            'industry_benchmark': industry_space_benchmark,
            'gap': space_utilization - industry_space_benchmark,
            'performance_vs_benchmark': (space_utilization / industry_space_benchmark) * 100
        },
        'supplier_performance': {
            'our_performance': supplier_performance,
            'industry_benchmark': industry_supplier_benchmark,
            'gap': supplier_performance - industry_supplier_benchmark,
            'performance_vs_benchmark': (supplier_performance / industry_supplier_benchmark) * 100
        }
    }
    
    # ===== PRICING BENCHMARKS =====
    print("Analyzing pricing benchmarks...")
    
    # Price elasticity benchmarks
    avg_elasticity = df['price_elasticity'].mean()
    industry_elasticity_benchmark = -1.2  # Industry benchmark (less elastic)
    
    # Promotional effectiveness benchmarks
    avg_promo_lift = df['promotional_lift'].mean()
    industry_promo_benchmark = 25.0  # Industry benchmark
    
    pricing_benchmarks = {
        'price_elasticity': {
            'our_performance': avg_elasticity,
            'industry_benchmark': industry_elasticity_benchmark,
            'gap': avg_elasticity - industry_elasticity_benchmark,
            'performance_vs_benchmark': abs(avg_elasticity / industry_elasticity_benchmark) * 100
        },
        'promotional_lift': {
            'our_performance': avg_promo_lift,
            'industry_benchmark': industry_promo_benchmark,
            'gap': avg_promo_lift - industry_promo_benchmark,
            'performance_vs_benchmark': (avg_promo_lift / industry_promo_benchmark) * 100
        }
    }
    
    # ===== CUSTOMER BENCHMARKS =====
    print("Analyzing customer benchmarks...")
    
    # Customer value benchmarks
    avg_transaction_value = df['total_amount'].mean()
    industry_transaction_benchmark = 45.0  # Industry benchmark
    
    # Basket size benchmarks
    avg_basket_size = df['basket_size'].mean()
    industry_basket_benchmark = 12.0  # Industry benchmark
    
    customer_benchmarks = {
        'transaction_value': {
            'our_performance': avg_transaction_value,
            'industry_benchmark': industry_transaction_benchmark,
            'gap': avg_transaction_value - industry_transaction_benchmark,
            'performance_vs_benchmark': (avg_transaction_value / industry_transaction_benchmark) * 100
        },
        'basket_size': {
            'our_performance': avg_basket_size,
            'industry_benchmark': industry_basket_benchmark,
            'gap': avg_basket_size - industry_basket_benchmark,
            'performance_vs_benchmark': (avg_basket_size / industry_basket_benchmark) * 100
        }
    }
    
    # Combine all benchmarks
    benchmarks = {
        'category_performance': industry_benchmarks['category_performance'],
        'operational_benchmarks': operational_benchmarks,
        'pricing_benchmarks': pricing_benchmarks,
        'customer_benchmarks': customer_benchmarks,
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save benchmarks
    output_path = "/Users/arghya.mukherjee/Downloads/cursor/sd/supply_chain/industry_benchmarks.json"
    with open(output_path, 'w') as f:
        json.dump(benchmarks, f, indent=2)
    
    print(f"Industry benchmarks saved to {output_path}")
    return benchmarks

if __name__ == "__main__":
    benchmarks = analyze_industry_benchmarks()
    
    print("\n" + "="*80)
    print("INDUSTRY BENCHMARK ANALYSIS")
    print("="*80)
    
    print("\nCATEGORY PERFORMANCE vs INDUSTRY:")
    for category, data in benchmarks['category_performance'].items():
        print(f"\n{category}:")
        print(f"  Revenue: ${data['our_revenue']:,.0f}")
        print(f"  Margin: {data['our_margin']:.1f}% vs Industry {data['industry_margin']:.1f}% (Gap: {data['gap_margin']:.1f}%)")
        print(f"  Turnover: {data['our_turnover']:.1f}x vs Industry {data['industry_turnover']:.1f}x (Gap: {data['gap_turnover']:.1f}x)")
    
    print("\nOPERATIONAL PERFORMANCE vs INDUSTRY:")
    for metric, data in benchmarks['operational_benchmarks'].items():
        print(f"  {metric.replace('_', ' ').title()}: {data['our_performance']:.1f} vs Industry {data['industry_benchmark']:.1f} ({data['performance_vs_benchmark']:.1f}%)")
    
    print("\nPRICING PERFORMANCE vs INDUSTRY:")
    for metric, data in benchmarks['pricing_benchmarks'].items():
        print(f"  {metric.replace('_', ' ').title()}: {data['our_performance']:.1f} vs Industry {data['industry_benchmark']:.1f} ({data['performance_vs_benchmark']:.1f}%)")
    
    print("\nCUSTOMER PERFORMANCE vs INDUSTRY:")
    for metric, data in benchmarks['customer_benchmarks'].items():
        print(f"  {metric.replace('_', ' ').title()}: {data['our_performance']:.1f} vs Industry {data['industry_benchmark']:.1f} ({data['performance_vs_benchmark']:.1f}%)")
