#!/usr/bin/env python3
"""
Phase 1.2B: CEO Executive Dashboard
10 comprehensive metric categories for CEO-level insights
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

def create_ceo_dashboard():
    print("=" * 80)
    print("PHASE 1.2B: CEO EXECUTIVE DASHBOARD")
    print("=" * 80)
    print()

    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/grocery_dataset.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year'] = df['timestamp'].dt.year
    df['quarter'] = df['timestamp'].dt.quarter
    df['month'] = df['timestamp'].dt.month
    df['year_month'] = df['timestamp'].dt.to_period('M')
    print(f"✓ Loaded {len(df):,} rows")
    print()

    dashboard_metrics = {}

    # ========================================================================
    # 1. BUSINESS PERFORMANCE
    # ========================================================================
    print("1. Business Performance Metrics...")

    total_revenue = df['total_amount'].sum()
    total_transactions = len(df)
    avg_transaction = df['total_amount'].mean()

    # By year
    yearly = df.groupby('year').agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    })

    # By quarter
    quarterly = df.groupby(['year', 'quarter']).agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    })

    # By month
    monthly = df.groupby('year_month').agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    })

    # Revenue per store
    revenue_per_store = total_revenue / df['store_id'].nunique()

    # Revenue per customer
    revenue_per_customer = total_revenue / df['customer_id'].nunique()

    # Transaction frequency per customer
    txn_per_customer = total_transactions / df['customer_id'].nunique()

    dashboard_metrics['business_performance'] = {
        'total_revenue_2_years': float(total_revenue),
        'total_revenue_2022': float(yearly.loc[2022, 'total_amount']),
        'total_revenue_2023': float(yearly.loc[2023, 'total_amount']),
        'total_transactions': int(total_transactions),
        'avg_transaction_value': float(avg_transaction),
        'revenue_per_store': float(revenue_per_store),
        'revenue_per_customer': float(revenue_per_customer),
        'transactions_per_customer': float(txn_per_customer)
    }

    # ========================================================================
    # 2. GROWTH METRICS
    # ========================================================================
    print("2. Growth Metrics...")

    # YoY Growth
    yoy_revenue_growth = ((yearly.loc[2023, 'total_amount'] - yearly.loc[2022, 'total_amount']) /
                          yearly.loc[2022, 'total_amount'] * 100)
    yoy_txn_growth = ((yearly.loc[2023, 'transaction_id'] - yearly.loc[2022, 'transaction_id']) /
                      yearly.loc[2022, 'transaction_id'] * 100)

    # Customer growth
    customers_2022 = df[df['year'] == 2022]['customer_id'].nunique()
    customers_2023 = df[df['year'] == 2023]['customer_id'].nunique()
    customer_growth = ((customers_2023 - customers_2022) / customers_2022 * 100)

    # QoQ Growth (Q4 2023 vs Q3 2023)
    q4_2023_revenue = quarterly.loc[(2023, 4), 'total_amount']
    q3_2023_revenue = quarterly.loc[(2023, 3), 'total_amount']
    qoq_growth = ((q4_2023_revenue - q3_2023_revenue) / q3_2023_revenue * 100)

    # MoM Growth (Dec 2023 vs Nov 2023)
    monthly_sorted = monthly.sort_index()
    last_month_rev = monthly_sorted.iloc[-1]['total_amount']
    prev_month_rev = monthly_sorted.iloc[-2]['total_amount']
    mom_growth = ((last_month_rev - prev_month_rev) / prev_month_rev * 100)

    dashboard_metrics['growth_metrics'] = {
        'yoy_revenue_growth_pct': float(yoy_revenue_growth),
        'yoy_transaction_growth_pct': float(yoy_txn_growth),
        'yoy_customer_growth_pct': float(customer_growth),
        'qoq_revenue_growth_pct': float(qoq_growth),
        'mom_revenue_growth_pct': float(mom_growth)
    }

    # ========================================================================
    # 3. OPERATIONAL METRICS
    # ========================================================================
    print("3. Operational Metrics...")

    store_count = df['store_id'].nunique()
    customer_count = df['customer_id'].nunique()
    product_count = df['product_id'].nunique()
    employee_count = df['employee_id'].nunique()
    avg_basket_size = df['basket_size'].mean()

    # By region
    stores_by_region = df.groupby('store_region')['store_id'].nunique().to_dict()

    # By type
    stores_by_type = df.groupby('store_type')['store_id'].nunique().to_dict()

    # Customers by segment
    customers_by_segment = df.groupby('customer_type')['customer_id'].nunique().to_dict()

    # Products by category
    products_by_category = df.groupby('category')['product_id'].nunique().to_dict()

    dashboard_metrics['operational_metrics'] = {
        'total_stores': int(store_count),
        'stores_by_region': {k: int(v) for k, v in stores_by_region.items()},
        'stores_by_type': {k: int(v) for k, v in stores_by_type.items()},
        'total_customers': int(customer_count),
        'customers_by_segment': {k: int(v) for k, v in customers_by_segment.items()},
        'total_products': int(product_count),
        'products_by_category': {k: int(v) for k, v in products_by_category.items()},
        'total_employees': int(employee_count),
        'avg_basket_size': float(avg_basket_size)
    }

    # ========================================================================
    # 4. PROFITABILITY INDICATORS
    # ========================================================================
    print("4. Profitability Indicators...")

    # Gross margin calculation
    total_unit_price = (df['unit_price'] * df['quantity']).sum()
    total_final_price = (df['final_price'] * df['quantity']).sum()
    gross_margin_pct = ((total_unit_price - total_final_price) / total_unit_price * 100)

    # Discount impact
    total_discounts = total_unit_price - total_final_price
    avg_discount_pct = df['discount_percentage'].mean()

    # Promotional transactions
    promo_count = (df['promotion_id'] != 'NO_PROMO').sum()
    promo_pct = (promo_count / len(df)) * 100
    promo_revenue = df[df['promotion_id'] != 'NO_PROMO']['total_amount'].sum()

    dashboard_metrics['profitability_indicators'] = {
        'gross_margin_pct': float(gross_margin_pct),
        'total_discounts_given': float(total_discounts),
        'avg_discount_pct': float(avg_discount_pct),
        'promotional_transaction_pct': float(promo_pct),
        'promotional_revenue': float(promo_revenue),
        'promotional_revenue_pct': float((promo_revenue / total_revenue) * 100)
    }

    # ========================================================================
    # 5. CUSTOMER METRICS
    # ========================================================================
    print("5. Customer Metrics...")

    # CLV (simplified: total revenue / unique customers)
    clv = revenue_per_customer

    # Customer segmentation revenue
    segment_revenue = df.groupby('customer_type')['total_amount'].sum()
    segment_customers = df.groupby('customer_type')['customer_id'].nunique()

    # Loyalty program usage
    loyalty_users = (df['loyalty_points_used'] > 0).sum()
    loyalty_usage_pct = (loyalty_users / len(df)) * 100

    # Retention (customers in both years)
    customers_both_years = len(set(df[df['year'] == 2022]['customer_id']) &
                               set(df[df['year'] == 2023]['customer_id']))
    retention_rate = (customers_both_years / customers_2022) * 100

    dashboard_metrics['customer_metrics'] = {
        'customer_lifetime_value': float(clv),
        'customer_retention_rate_pct': float(retention_rate),
        'loyalty_program_usage_pct': float(loyalty_usage_pct),
        'segment_breakdown': {
            seg: {
                'revenue': float(segment_revenue[seg]),
                'customers': int(segment_customers[seg]),
                'avg_revenue_per_customer': float(segment_revenue[seg] / segment_customers[seg])
            } for seg in segment_revenue.index
        }
    }

    # ========================================================================
    # 6. PRODUCT PERFORMANCE
    # ========================================================================
    print("6. Product Performance...")

    # Top 10 products by revenue
    top_products_rev = df.groupby(['product_id', 'product_name']).agg({
        'total_amount': 'sum',
        'quantity': 'sum'
    }).sort_values('total_amount', ascending=False).head(10)

    # Top 10 products by volume
    top_products_vol = df.groupby(['product_id', 'product_name']).agg({
        'total_amount': 'sum',
        'quantity': 'sum'
    }).sort_values('quantity', ascending=False).head(10)

    # Top 10 categories by revenue
    top_categories = df.groupby('category')['total_amount'].sum().sort_values(ascending=False).head(10)

    # Growth analysis by product (2023 vs 2022)
    product_growth = []
    for pid in df['product_id'].unique()[:20]:  # Sample top products
        prod_2022 = df[(df['product_id'] == pid) & (df['year'] == 2022)]['total_amount'].sum()
        prod_2023 = df[(df['product_id'] == pid) & (df['year'] == 2023)]['total_amount'].sum()
        if prod_2022 > 0:
            growth = ((prod_2023 - prod_2022) / prod_2022 * 100)
            product_growth.append({
                'product_id': pid,
                'product_name': df[df['product_id'] == pid]['product_name'].iloc[0],
                'growth_pct': growth,
                'revenue_2023': prod_2023
            })

    product_growth_sorted = sorted(product_growth, key=lambda x: x['growth_pct'], reverse=True)

    dashboard_metrics['product_performance'] = {
        'top_10_by_revenue': [
            {'product_id': idx[0], 'product_name': idx[1], 'revenue': float(row['total_amount'])}
            for idx, row in top_products_rev.iterrows()
        ],
        'top_10_by_volume': [
            {'product_id': idx[0], 'product_name': idx[1], 'quantity': int(row['quantity'])}
            for idx, row in top_products_vol.iterrows()
        ],
        'top_10_categories': {cat: float(rev) for cat, rev in top_categories.items()},
        'fastest_growing_products': product_growth_sorted[:5]
    }

    # ========================================================================
    # 7. REGIONAL PERFORMANCE
    # ========================================================================
    print("7. Regional Performance...")

    regional = df.groupby('store_region').agg({
        'total_amount': 'sum',
        'store_id': 'nunique',
        'customer_id': 'nunique',
        'transaction_id': 'count'
    }).sort_values('total_amount', ascending=False)

    dashboard_metrics['regional_performance'] = {
        region: {
            'revenue': float(row['total_amount']),
            'revenue_pct': float((row['total_amount'] / total_revenue) * 100),
            'stores': int(row['store_id']),
            'customers': int(row['customer_id']),
            'transactions': int(row['transaction_id']),
            'revenue_per_store': float(row['total_amount'] / row['store_id'])
        }
        for region, row in regional.iterrows()
    }

    # ========================================================================
    # 8. CHANNEL PERFORMANCE
    # ========================================================================
    print("8. Channel Performance...")

    # Delivery method
    delivery = df.groupby('delivery_method')['total_amount'].sum()

    # Payment method
    payment = df.groupby('payment_method')['total_amount'].sum()

    # Organic vs Non-organic
    organic_rev = df[df['is_organic'] == True]['total_amount'].sum()
    non_organic_rev = df[df['is_organic'] == False]['total_amount'].sum()

    dashboard_metrics['channel_performance'] = {
        'delivery_method': {method: float(rev) for method, rev in delivery.items()},
        'payment_method': {method: float(rev) for method, rev in payment.items()},
        'organic_vs_nonorganic': {
            'organic_revenue': float(organic_rev),
            'organic_pct': float((organic_rev / total_revenue) * 100),
            'non_organic_revenue': float(non_organic_rev),
            'non_organic_pct': float((non_organic_rev / total_revenue) * 100)
        }
    }

    # ========================================================================
    # 9. TIME-BASED PATTERNS
    # ========================================================================
    print("9. Time-Based Patterns...")

    # Weekend vs Weekday
    weekend_rev = df[df['is_weekend'] == True]['total_amount'].sum()
    weekday_rev = df[df['is_weekend'] == False]['total_amount'].sum()

    # Seasonal
    seasonal = df.groupby('season')['total_amount'].sum().sort_values(ascending=False)

    # Time slot
    timeslot = df.groupby('time_slot')['total_amount'].sum().sort_values(ascending=False)

    # Monthly trends
    monthly_trends = df.groupby('year_month').agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    monthly_trends['year_month'] = monthly_trends['year_month'].astype(str)

    dashboard_metrics['time_based_patterns'] = {
        'weekend_vs_weekday': {
            'weekend_revenue': float(weekend_rev),
            'weekend_pct': float((weekend_rev / total_revenue) * 100),
            'weekday_revenue': float(weekday_rev),
            'weekday_pct': float((weekday_rev / total_revenue) * 100)
        },
        'seasonal': {season: float(rev) for season, rev in seasonal.items()},
        'time_slot': {slot: float(rev) for slot, rev in timeslot.items()},
        'monthly_trends': monthly_trends.to_dict('records')
    }

    # ========================================================================
    # 10. OPERATIONAL EFFICIENCY
    # ========================================================================
    print("10. Operational Efficiency...")

    avg_checkout_duration = df['checkout_duration_sec'].mean()

    # Peak hour analysis
    df['hour'] = df['timestamp'].dt.hour
    hourly_traffic = df.groupby('hour')['transaction_id'].count().sort_values(ascending=False)

    # Employee productivity
    emp_productivity = df.groupby('employee_id').agg({
        'transaction_id': 'count',
        'total_amount': 'sum'
    })
    avg_txn_per_employee = emp_productivity['transaction_id'].mean()
    avg_revenue_per_employee = emp_productivity['total_amount'].mean()

    # Stock turnover (simplified)
    avg_stock_level = df['stock_level_at_sale'].mean()

    dashboard_metrics['operational_efficiency'] = {
        'avg_checkout_duration_sec': float(avg_checkout_duration),
        'peak_hours': [
            {'hour': int(hour), 'transactions': int(count)}
            for hour, count in hourly_traffic.head(5).items()
        ],
        'avg_transactions_per_employee': float(avg_txn_per_employee),
        'avg_revenue_per_employee': float(avg_revenue_per_employee),
        'avg_stock_level_at_sale': float(avg_stock_level)
    }

    # ========================================================================
    # SAVE DASHBOARD
    # ========================================================================
    print()
    print("=" * 80)
    print("SAVING CEO EXECUTIVE DASHBOARD")
    print("=" * 80)

    # Save as JSON
    json_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/ceo_executive_dashboard.json'
    with open(json_path, 'w') as f:
        json.dump(dashboard_metrics, f, indent=2)
    print(f"✓ JSON dashboard saved: {json_path}")

    # Create flattened CSV for easy viewing
    csv_data = []

    def flatten_dict(d, prefix=''):
        for key, value in d.items():
            if isinstance(value, dict):
                flatten_dict(value, f"{prefix}{key}.")
            elif isinstance(value, list):
                csv_data.append({
                    'metric_category': prefix.rstrip('.'),
                    'metric_name': key,
                    'value': str(value)
                })
            else:
                csv_data.append({
                    'metric_category': prefix.rstrip('.'),
                    'metric_name': key,
                    'value': value
                })

    flatten_dict(dashboard_metrics)

    csv_df = pd.DataFrame(csv_data)
    csv_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/ceo_executive_dashboard.csv'
    csv_df.to_csv(csv_path, index=False)
    print(f"✓ CSV dashboard saved: {csv_path}")

    # Create summary markdown
    summary_md = f"""# CEO Executive Dashboard
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. BUSINESS PERFORMANCE
- **Total Revenue (2 years)**: ${dashboard_metrics['business_performance']['total_revenue_2_years']:,.2f}
- **2022 Revenue**: ${dashboard_metrics['business_performance']['total_revenue_2022']:,.2f}
- **2023 Revenue**: ${dashboard_metrics['business_performance']['total_revenue_2023']:,.2f}
- **Total Transactions**: {dashboard_metrics['business_performance']['total_transactions']:,}
- **Avg Transaction Value**: ${dashboard_metrics['business_performance']['avg_transaction_value']:.2f}
- **Revenue per Store**: ${dashboard_metrics['business_performance']['revenue_per_store']:,.2f}
- **Revenue per Customer**: ${dashboard_metrics['business_performance']['revenue_per_customer']:.2f}

## 2. GROWTH METRICS
- **YoY Revenue Growth**: {dashboard_metrics['growth_metrics']['yoy_revenue_growth_pct']:.2f}%
- **YoY Transaction Growth**: {dashboard_metrics['growth_metrics']['yoy_transaction_growth_pct']:.2f}%
- **YoY Customer Growth**: {dashboard_metrics['growth_metrics']['yoy_customer_growth_pct']:.2f}%
- **QoQ Revenue Growth**: {dashboard_metrics['growth_metrics']['qoq_revenue_growth_pct']:.2f}%
- **MoM Revenue Growth**: {dashboard_metrics['growth_metrics']['mom_revenue_growth_pct']:.2f}%

## 3. OPERATIONAL METRICS
- **Total Stores**: {dashboard_metrics['operational_metrics']['total_stores']}
- **Total Customers**: {dashboard_metrics['operational_metrics']['total_customers']:,}
- **Total Products**: {dashboard_metrics['operational_metrics']['total_products']}
- **Total Employees**: {dashboard_metrics['operational_metrics']['total_employees']}
- **Avg Basket Size**: {dashboard_metrics['operational_metrics']['avg_basket_size']:.2f} items

## 4. PROFITABILITY INDICATORS
- **Gross Margin**: {dashboard_metrics['profitability_indicators']['gross_margin_pct']:.2f}%
- **Total Discounts Given**: ${dashboard_metrics['profitability_indicators']['total_discounts_given']:,.2f}
- **Avg Discount**: {dashboard_metrics['profitability_indicators']['avg_discount_pct']:.2f}%
- **Promotional Transaction %**: {dashboard_metrics['profitability_indicators']['promotional_transaction_pct']:.2f}%

## 5. CUSTOMER METRICS
- **Customer Lifetime Value**: ${dashboard_metrics['customer_metrics']['customer_lifetime_value']:.2f}
- **Customer Retention Rate**: {dashboard_metrics['customer_metrics']['customer_retention_rate_pct']:.2f}%
- **Loyalty Program Usage**: {dashboard_metrics['customer_metrics']['loyalty_program_usage_pct']:.2f}%

## 6-10. Additional Metrics
See full JSON file for:
- Product Performance
- Regional Performance
- Channel Performance
- Time-Based Patterns
- Operational Efficiency

---
**Dashboard Complete**: 10 comprehensive metric categories analyzed
"""

    md_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/descriptive_analytics_summary.md'
    with open(md_path, 'w') as f:
        f.write(summary_md)
    print(f"✓ Summary markdown saved: {md_path}")

    print()
    print("=" * 80)
    print("✅ CEO EXECUTIVE DASHBOARD COMPLETE!")
    print("=" * 80)
    print(f"Total Metrics Categories: 10")
    print(f"Files Created: 3 (JSON, CSV, MD)")

    return dashboard_metrics

if __name__ == "__main__":
    dashboard = create_ceo_dashboard()
