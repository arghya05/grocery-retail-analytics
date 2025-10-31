#!/usr/bin/env python3
"""
Phase 1.3: Predictive Analytics
Revenue forecasting, customer behavior prediction, risk & opportunity identification
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def predictive_analytics():
    print("=" * 80)
    print("PHASE 1.3: PREDICTIVE ANALYTICS")
    print("=" * 80)
    print()

    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/grocery_dataset.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year'] = df['timestamp'].dt.year
    df['quarter'] = df['timestamp'].dt.quarter
    df['month'] = df['timestamp'].dt.month
    df['year_quarter'] = df['year'].astype(str) + '-Q' + df['quarter'].astype(str)
    print(f"✓ Loaded {len(df):,} rows")
    print()

    predictions = {}

    # ========================================================================
    # 1. REVENUE FORECASTING
    # ========================================================================
    print("1. Revenue Forecasting...")

    # Quarterly revenue trend
    quarterly = df.groupby('year_quarter')['total_amount'].sum().sort_index()
    print(f"\nHistorical Quarterly Revenue:")
    for quarter, rev in quarterly.items():
        print(f"  {quarter}: ${rev:,.2f}")

    # Calculate growth rate
    q_revenues = quarterly.values
    avg_growth_rate = np.mean([(q_revenues[i] - q_revenues[i-1]) / q_revenues[i-1]
                                for i in range(1, len(q_revenues))])

    # Forecast next 4 quarters (2024)
    last_quarter_rev = quarterly.iloc[-1]
    forecasts_q = []

    print(f"\nAverage QoQ Growth Rate: {avg_growth_rate*100:.2f}%")
    print(f"\nForecasted Quarterly Revenue (2024):")

    for i in range(1, 5):
        forecast_rev = last_quarter_rev * ((1 + avg_growth_rate) ** i)
        quarter_name = f"2024-Q{i}"
        forecasts_q.append({
            'quarter': quarter_name,
            'forecasted_revenue': float(forecast_rev),
            'growth_assumption_pct': float(avg_growth_rate * 100)
        })
        print(f"  {quarter_name}: ${forecast_rev:,.2f}")

    # Annual projection
    annual_2024_forecast = sum(f['forecasted_revenue'] for f in forecasts_q)
    annual_2023 = df[df['year'] == 2023]['total_amount'].sum()
    annual_2022 = df[df['year'] == 2022]['total_amount'].sum()

    print(f"\nAnnual Revenue:")
    print(f"  2022 (Actual): ${annual_2022:,.2f}")
    print(f"  2023 (Actual): ${annual_2023:,.2f}")
    print(f"  2024 (Forecast): ${annual_2024_forecast:,.2f}")
    print(f"  2024 YoY Growth: {((annual_2024_forecast - annual_2023) / annual_2023 * 100):.2f}%")

    # Seasonality patterns
    seasonal = df.groupby('season')['total_amount'].sum()
    seasonal_pct = (seasonal / seasonal.sum() * 100)

    predictions['revenue_forecasting'] = {
        'next_4_quarters': forecasts_q,
        'annual_2024_forecast': float(annual_2024_forecast),
        'annual_2024_growth_pct': float((annual_2024_forecast - annual_2023) / annual_2023 * 100),
        'avg_quarterly_growth_rate_pct': float(avg_growth_rate * 100),
        'seasonality_patterns': {
            season: {
                'revenue': float(rev),
                'percentage': float(seasonal_pct[season])
            } for season, rev in seasonal.items()
        }
    }

    # ========================================================================
    # 2. CUSTOMER BEHAVIOR PREDICTION
    # ========================================================================
    print("\n2. Customer Behavior Prediction...")

    # Customer frequency analysis
    customer_txn_count = df.groupby('customer_id').size()

    # Churn risk (customers with declining frequency)
    h1_2023 = df[(df['year'] == 2023) & (df['month'] <= 6)].groupby('customer_id').size()
    h2_2023 = df[(df['year'] == 2023) & (df['month'] > 6)].groupby('customer_id').size()

    # Find customers with declining activity
    declining_customers = []
    for cid in h1_2023.index:
        h1_count = h1_2023.get(cid, 0)
        h2_count = h2_2023.get(cid, 0)
        if h2_count < h1_count * 0.5:  # 50% decline
            decline_pct = ((h1_count - h2_count) / h1_count * 100)
            declining_customers.append({
                'customer_id': cid,
                'h1_2023_transactions': int(h1_count),
                'h2_2023_transactions': int(h2_count),
                'decline_pct': float(decline_pct),
                'churn_risk': 'HIGH' if decline_pct > 75 else 'MEDIUM'
            })

    declining_customers = sorted(declining_customers, key=lambda x: x['decline_pct'], reverse=True)
    high_churn_risk_count = len([c for c in declining_customers if c['churn_risk'] == 'HIGH'])

    print(f"  Customers at Churn Risk: {len(declining_customers):,}")
    print(f"  High Churn Risk: {high_churn_risk_count:,}")

    # Customer segment migration
    segment_2022 = df[df['year'] == 2022].groupby('customer_id')['customer_type'].first()
    segment_2023 = df[df['year'] == 2023].groupby('customer_id')['customer_type'].first()

    # Common customers
    common_custs = set(segment_2022.index) & set(segment_2023.index)
    migrations = []
    for cid in list(common_custs)[:1000]:  # Sample
        seg_2022 = segment_2022[cid]
        seg_2023 = segment_2023[cid]
        if seg_2022 != seg_2023:
            migrations.append({
                'from_segment': seg_2022,
                'to_segment': seg_2023
            })

    migration_summary = {}
    for m in migrations:
        key = f"{m['from_segment']} → {m['to_segment']}"
        migration_summary[key] = migration_summary.get(key, 0) + 1

    print(f"  Customer Segment Migrations: {len(migrations)} (sample)")

    # CLV projections
    avg_clv_by_segment = df.groupby('customer_type').apply(
        lambda x: x['total_amount'].sum() / x['customer_id'].nunique()
    )

    predictions['customer_behavior'] = {
        'churn_risk_analysis': {
            'total_at_risk': len(declining_customers),
            'high_risk_count': high_churn_risk_count,
            'medium_risk_count': len(declining_customers) - high_churn_risk_count,
            'top_20_at_risk': declining_customers[:20]
        },
        'segment_migration': migration_summary,
        'clv_by_segment': {seg: float(clv) for seg, clv in avg_clv_by_segment.items()}
    }

    # ========================================================================
    # 3. PRODUCT DEMAND FORECASTING
    # ========================================================================
    print("\n3. Product Demand Forecasting...")

    # Top products with growth trends
    product_2022 = df[df['year'] == 2022].groupby('product_id')['total_amount'].sum()
    product_2023 = df[df['year'] == 2023].groupby('product_id')['total_amount'].sum()

    product_forecasts = []
    for pid in df['product_id'].unique():
        rev_2022 = product_2022.get(pid, 0)
        rev_2023 = product_2023.get(pid, 0)

        if rev_2022 > 0:
            growth = ((rev_2023 - rev_2022) / rev_2022)
            forecast_2024 = rev_2023 * (1 + growth)

            product_forecasts.append({
                'product_id': pid,
                'product_name': df[df['product_id'] == pid]['product_name'].iloc[0],
                'category': df[df['product_id'] == pid]['category'].iloc[0],
                'revenue_2022': float(rev_2022),
                'revenue_2023': float(rev_2023),
                'growth_pct': float(growth * 100),
                'forecast_2024': float(forecast_2024)
            })

    # Sort by growth
    fast_moving = sorted(product_forecasts, key=lambda x: x['growth_pct'], reverse=True)[:10]
    slow_moving = sorted(product_forecasts, key=lambda x: x['growth_pct'])[:10]

    print(f"  Fastest Growing Products (Top 10):")
    for p in fast_moving[:5]:
        print(f"    {p['product_name']}: {p['growth_pct']:.1f}% growth")

    # Category growth predictions
    category_2022 = df[df['year'] == 2022].groupby('category')['total_amount'].sum()
    category_2023 = df[df['year'] == 2023].groupby('category')['total_amount'].sum()

    category_forecasts = {}
    for cat in df['category'].unique():
        rev_2022 = category_2022.get(cat, 0)
        rev_2023 = category_2023.get(cat, 0)
        if rev_2022 > 0:
            growth = ((rev_2023 - rev_2022) / rev_2022)
            forecast_2024 = rev_2023 * (1 + growth)
            category_forecasts[cat] = {
                'revenue_2023': float(rev_2023),
                'growth_pct': float(growth * 100),
                'forecast_2024': float(forecast_2024)
            }

    predictions['product_demand'] = {
        'fastest_growing_products': fast_moving,
        'slowest_growing_products': slow_moving,
        'category_forecasts': category_forecasts
    }

    # ========================================================================
    # 4. RISK IDENTIFICATION
    # ========================================================================
    print("\n4. Risk Identification...")

    # Declining stores
    store_2022 = df[df['year'] == 2022].groupby('store_id')['total_amount'].sum()
    store_2023 = df[df['year'] == 2023].groupby('store_id')['total_amount'].sum()

    declining_stores = []
    for sid in df['store_id'].unique():
        rev_2022 = store_2022.get(sid, 0)
        rev_2023 = store_2023.get(sid, 0)
        if rev_2022 > 0:
            change = ((rev_2023 - rev_2022) / rev_2022 * 100)
            if change < -5:  # Declining by more than 5%
                declining_stores.append({
                    'store_id': sid,
                    'region': df[df['store_id'] == sid]['store_region'].iloc[0],
                    'store_type': df[df['store_id'] == sid]['store_type'].iloc[0],
                    'revenue_2022': float(rev_2022),
                    'revenue_2023': float(rev_2023),
                    'decline_pct': float(change),
                    'revenue_at_risk': float(rev_2022 - rev_2023)
                })

    declining_stores = sorted(declining_stores, key=lambda x: x['decline_pct'])
    total_revenue_at_risk = sum(s['revenue_at_risk'] for s in declining_stores)

    print(f"  Declining Stores: {len(declining_stores)}")
    print(f"  Total Revenue at Risk: ${total_revenue_at_risk:,.2f}")

    # Declining categories
    declining_categories = []
    for cat in df['category'].unique():
        rev_2022 = category_2022.get(cat, 0)
        rev_2023 = category_2023.get(cat, 0)
        if rev_2022 > 0:
            change = ((rev_2023 - rev_2022) / rev_2022 * 100)
            if change < 0:
                declining_categories.append({
                    'category': cat,
                    'revenue_2022': float(rev_2022),
                    'revenue_2023': float(rev_2023),
                    'decline_pct': float(change)
                })

    predictions['risk_identification'] = {
        'revenue_at_risk': {
            'total_amount': float(total_revenue_at_risk),
            'declining_stores_count': len(declining_stores),
            'declining_stores': declining_stores
        },
        'customers_at_risk': {
            'total_count': len(declining_customers),
            'high_risk_count': high_churn_risk_count
        },
        'declining_categories': declining_categories
    }

    # ========================================================================
    # 5. OPPORTUNITY IDENTIFICATION
    # ========================================================================
    print("\n5. Opportunity Identification...")

    # High-growth potential stores
    growing_stores = []
    for sid in df['store_id'].unique():
        rev_2022 = store_2022.get(sid, 0)
        rev_2023 = store_2023.get(sid, 0)
        if rev_2022 > 0:
            growth = ((rev_2023 - rev_2022) / rev_2022 * 100)
            if growth > 10:  # Growing by more than 10%
                growing_stores.append({
                    'store_id': sid,
                    'region': df[df['store_id'] == sid]['store_region'].iloc[0],
                    'store_type': df[df['store_id'] == sid]['store_type'].iloc[0],
                    'revenue_2023': float(rev_2023),
                    'growth_pct': float(growth),
                    'growth_potential': 'HIGH' if growth > 20 else 'MEDIUM'
                })

    growing_stores = sorted(growing_stores, key=lambda x: x['growth_pct'], reverse=True)

    print(f"  High-Growth Stores: {len(growing_stores)}")
    if growing_stores:
        print(f"  Top Growth Store: {growing_stores[0]['store_id']} ({growing_stores[0]['growth_pct']:.1f}%)")

    # Cross-sell opportunities (customers buying only from few categories)
    customer_categories = df.groupby('customer_id')['category'].nunique()
    low_diversity_customers = customer_categories[customer_categories <= 3]

    print(f"  Cross-sell Opportunities: {len(low_diversity_customers):,} customers")

    predictions['opportunity_identification'] = {
        'high_growth_stores': growing_stores,
        'underperforming_with_potential': [
            s for s in declining_stores if s['revenue_2022'] > 50000000  # High revenue stores declining
        ],
        'cross_sell_opportunities': {
            'customers_with_low_category_diversity': int(len(low_diversity_customers)),
            'average_categories_per_customer': float(customer_categories.mean())
        }
    }

    # ========================================================================
    # SAVE RESULTS
    # ========================================================================
    print()
    print("=" * 80)
    print("SAVING PREDICTIVE ANALYTICS")
    print("=" * 80)

    # Save JSON
    json_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/predictive_analytics_forecasts.json'
    with open(json_path, 'w') as f:
        json.dump(predictions, f, indent=2)
    print(f"✓ Predictions JSON saved: {json_path}")

    # Save quarterly forecasts CSV
    forecast_df = pd.DataFrame(forecasts_q)
    forecast_csv = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_forecast_next_4_quarters.csv'
    forecast_df.to_csv(forecast_csv, index=False)
    print(f"✓ Quarterly forecast CSV saved: {forecast_csv}")

    # Save churn risk CSV
    churn_df = pd.DataFrame(declining_customers)
    churn_csv = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/customer_churn_risk.csv'
    churn_df.to_csv(churn_csv, index=False)
    print(f"✓ Churn risk CSV saved: {churn_csv}")

    # Create summary markdown
    summary = f"""# Predictive Analytics Insights
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Revenue Forecasting

### 2024 Annual Forecast
- **Forecasted Revenue**: ${annual_2024_forecast:,.2f}
- **Expected YoY Growth**: {((annual_2024_forecast - annual_2023) / annual_2023 * 100):.2f}%
- **Average Quarterly Growth Rate**: {avg_growth_rate * 100:.2f}%

### Quarterly Forecasts (2024)
"""
    for f in forecasts_q:
        summary += f"- **{f['quarter']}**: ${f['forecasted_revenue']:,.2f}\n"

    summary += f"""
## Customer Behavior Predictions

- **Customers at Churn Risk**: {len(declining_customers):,}
  - High Risk: {high_churn_risk_count:,}
  - Medium Risk: {len(declining_customers) - high_churn_risk_count:,}

- **Cross-sell Opportunities**: {len(low_diversity_customers):,} customers with low category diversity

## Risk Identification

- **Total Revenue at Risk**: ${total_revenue_at_risk:,.2f}
- **Declining Stores**: {len(declining_stores)}
- **Declining Categories**: {len(declining_categories)}

## Opportunity Identification

- **High-Growth Stores**: {len(growing_stores)}
- **Fastest Growing Products**: {len(fast_moving)} identified
- **Growth Potential**: Significant opportunities in store expansion and product optimization

---
**Analysis Method**: Time series trend analysis with YoY growth extrapolation
**Confidence Level**: Medium (based on 2-year historical data)
"""

    md_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/predictive_insights_summary.md'
    with open(md_path, 'w') as f:
        f.write(summary)
    print(f"✓ Summary markdown saved: {md_path}")

    print()
    print("=" * 80)
    print("✅ PREDICTIVE ANALYTICS COMPLETE!")
    print("=" * 80)
    print(f"2024 Revenue Forecast: ${annual_2024_forecast:,.2f}")
    print(f"Customers at Risk: {len(declining_customers):,}")
    print(f"Growth Opportunities: {len(growing_stores)} stores")
    print(f"Files Created: 4 (JSON, 2 CSVs, MD)")

    return predictions

if __name__ == "__main__":
    predictions = predictive_analytics()
