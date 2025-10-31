#!/usr/bin/env python3
"""
Phase 1.5: Granular Deep-Dive Insights
Top/Bottom stores, products, customer segments, categories, regional analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime

def granular_insights():
    print("=" * 80)
    print("PHASE 1.5: GRANULAR DEEP-DIVE INSIGHTS")
    print("=" * 80)
    print()

    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/grocery_dataset.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year'] = df['timestamp'].dt.year
    print(f"✓ Loaded {len(df):,} rows")
    print()

    # ========================================================================
    # 1. STORE-LEVEL INSIGHTS
    # ========================================================================
    print("1. Store-Level Insights (Top 50 + Bottom 50)...")

    store_analysis = df.groupby(['store_id', 'store_region', 'store_type']).agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum',
        'discount_percentage': 'mean',
        'basket_size': 'mean',
        'checkout_duration_sec': 'mean'
    }).reset_index()

    store_analysis.columns = ['store_id', 'region', 'store_type', 'revenue', 'transactions',
                               'unique_customers', 'units_sold', 'avg_discount_pct',
                               'avg_basket_size', 'avg_checkout_sec']

    store_analysis['revenue_per_transaction'] = store_analysis['revenue'] / store_analysis['transactions']
    store_analysis['revenue_per_customer'] = store_analysis['revenue'] / store_analysis['unique_customers']

    # YoY growth for stores
    store_2022 = df[df['year'] == 2022].groupby('store_id')['total_amount'].sum()
    store_2023 = df[df['year'] == 2023].groupby('store_id')['total_amount'].sum()

    store_analysis['yoy_growth_pct'] = store_analysis['store_id'].apply(
        lambda x: ((store_2023.get(x, 0) - store_2022.get(x, 0)) / store_2022.get(x, 1) * 100)
        if store_2022.get(x, 0) > 0 else 0
    )

    # Top 50 stores
    top_50_stores = store_analysis.nlargest(50, 'revenue').copy()
    top_50_stores['performance_tier'] = 'TOP_50'

    # Add strategic recommendations for top stores
    def get_store_recommendation(row):
        if row['yoy_growth_pct'] > 5:
            return "EXPAND - High growth momentum, consider opening similar format store in region"
        elif row['revenue_per_customer'] > store_analysis['revenue_per_customer'].median():
            return "OPTIMIZE - Strong customer value, increase customer acquisition"
        else:
            return "MAINTAIN - Stable performance, focus on operational efficiency"

    top_50_stores['recommendation'] = top_50_stores.apply(get_store_recommendation, axis=1)

    # Bottom 50 stores
    bottom_50_stores = store_analysis.nsmallest(50, 'revenue').copy()
    bottom_50_stores['performance_tier'] = 'BOTTOM_50'

    def get_bottom_store_recommendation(row):
        if row['yoy_growth_pct'] < -10:
            return "CRITICAL - Severe decline, conduct immediate intervention or consider closure"
        elif row['revenue_per_transaction'] < store_analysis['revenue_per_transaction'].quantile(0.25):
            return "IMPROVE - Low transaction value, enhance product mix and upsell strategies"
        else:
            return "MONITOR - Underperforming but stable, implement 90-day improvement plan"

    bottom_50_stores['recommendation'] = bottom_50_stores.apply(get_bottom_store_recommendation, axis=1)

    # Save
    top_50_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/store_insights_top_50.csv'
    top_50_stores.to_csv(top_50_path, index=False)
    print(f"✓ Top 50 stores saved: {top_50_path}")

    bottom_50_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/store_insights_bottom_50.csv'
    bottom_50_stores.to_csv(bottom_50_path, index=False)
    print(f"✓ Bottom 50 stores saved: {bottom_50_path}")

    # ========================================================================
    # 2. PRODUCT-LEVEL INSIGHTS
    # ========================================================================
    print("\n2. Product-Level Insights (Top 100)...")

    product_analysis = df.groupby(['product_id', 'product_name', 'category', 'sub_category', 'brand']).agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum',
        'unit_price': 'mean',
        'discount_percentage': 'mean',
        'final_price': 'mean'
    }).reset_index()

    product_analysis.columns = ['product_id', 'product_name', 'category', 'sub_category', 'brand',
                                 'revenue', 'transactions', 'unique_customers', 'units_sold',
                                 'avg_unit_price', 'avg_discount_pct', 'avg_final_price']

    # Growth analysis
    prod_2022 = df[df['year'] == 2022].groupby('product_id')['total_amount'].sum()
    prod_2023 = df[df['year'] == 2023].groupby('product_id')['total_amount'].sum()

    product_analysis['yoy_growth_pct'] = product_analysis['product_id'].apply(
        lambda x: ((prod_2023.get(x, 0) - prod_2022.get(x, 0)) / prod_2022.get(x, 1) * 100)
        if prod_2022.get(x, 0) > 0 else 0
    )

    # Margin calculation
    product_analysis['gross_margin_pct'] = (
        (product_analysis['avg_unit_price'] - product_analysis['avg_final_price']) /
        product_analysis['avg_unit_price'] * 100
    )

    # Strategic classification
    def classify_product(row):
        if row['revenue'] > product_analysis['revenue'].quantile(0.8) and row['yoy_growth_pct'] > 5:
            return "STAR - High revenue, high growth"
        elif row['revenue'] > product_analysis['revenue'].quantile(0.8):
            return "CASH_COW - High revenue, stable"
        elif row['yoy_growth_pct'] > 10:
            return "RISING_STAR - Growing fast"
        elif row['yoy_growth_pct'] < -5:
            return "DECLINING - Consider discontinuation"
        else:
            return "STEADY - Maintain"

    product_analysis['classification'] = product_analysis.apply(classify_product, axis=1)

    # Top 100 products
    top_100_products = product_analysis.nlargest(100, 'revenue')

    top_100_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/product_insights_top_100.csv'
    top_100_products.to_csv(top_100_path, index=False)
    print(f"✓ Top 100 products saved: {top_100_path}")

    # ========================================================================
    # 3. CUSTOMER SEGMENT INSIGHTS
    # ========================================================================
    print("\n3. Customer Segment Deep Dive...")

    segment_insights = {}

    for segment in df['customer_type'].unique():
        seg_df = df[df['customer_type'] == segment]

        insights = {
            'segment_name': segment,
            'customer_count': int(seg_df['customer_id'].nunique()),
            'total_revenue': float(seg_df['total_amount'].sum()),
            'total_transactions': int(len(seg_df)),
            'avg_transaction_value': float(seg_df['total_amount'].mean()),
            'avg_basket_size': float(seg_df['basket_size'].mean()),
            'avg_discount_used': float(seg_df['discount_percentage'].mean()),
            'loyalty_program_usage_pct': float((seg_df['loyalty_points_used'] > 0).sum() / len(seg_df) * 100),
            'organic_preference_pct': float((seg_df['is_organic'] == True).sum() / len(seg_df) * 100),
            'home_delivery_pct': float((seg_df['delivery_method'] == 'Home Delivery').sum() / len(seg_df) * 100),
            'weekend_shopping_pct': float(seg_df['is_weekend'].sum() / len(seg_df) * 100),
        }

        # Top categories for this segment
        top_cats = seg_df.groupby('category')['total_amount'].sum().nlargest(5)
        insights['top_categories'] = {cat: float(rev) for cat, rev in top_cats.items()}

        # Demographics
        age_dist = seg_df.groupby('age_group').size()
        insights['age_distribution'] = {age: int(count) for age, count in age_dist.items()}

        gender_dist = seg_df.groupby('gender').size()
        insights['gender_distribution'] = {gender: int(count) for gender, count in gender_dist.items()}

        # Behavioral patterns
        time_pref = seg_df.groupby('time_slot').size().idxmax()
        insights['preferred_time_slot'] = time_pref

        payment_pref = seg_df.groupby('payment_method').size().idxmax()
        insights['preferred_payment_method'] = payment_pref

        segment_insights[segment] = insights

    # Create markdown summary
    segment_md = f"""# Customer Segment Deep Dive
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

    for segment, insights in segment_insights.items():
        segment_md += f"""## {segment} Customers

### Profile
- **Customer Count**: {insights['customer_count']:,}
- **Total Revenue**: ${insights['total_revenue']:,.2f} ({insights['total_revenue']/df['total_amount'].sum()*100:.1f}% of total)
- **Avg Transaction Value**: ${insights['avg_transaction_value']:.2f}
- **Avg Basket Size**: {insights['avg_basket_size']:.1f} items

### Behavior
- **Loyalty Usage**: {insights['loyalty_program_usage_pct']:.1f}%
- **Organic Preference**: {insights['organic_preference_pct']:.1f}%
- **Home Delivery**: {insights['home_delivery_pct']:.1f}%
- **Weekend Shopping**: {insights['weekend_shopping_pct']:.1f}%
- **Preferred Time**: {insights['preferred_time_slot']}
- **Preferred Payment**: {insights['preferred_payment_method']}

### Top Categories
"""
        for i, (cat, rev) in enumerate(insights['top_categories'].items(), 1):
            segment_md += f"{i}. {cat}: ${rev:,.2f}\n"

        segment_md += "\n---\n\n"

    segment_md_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/customer_segment_deep_dive.md'
    with open(segment_md_path, 'w') as f:
        f.write(segment_md)
    print(f"✓ Customer segment deep dive saved: {segment_md_path}")

    # ========================================================================
    # 4. CATEGORY DEEP-DIVES
    # ========================================================================
    print("\n4. Category Deep-Dives (All 10 categories)...")

    category_md = f"""# Category Deep-Dive Analysis
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

    for category in df['category'].unique():
        cat_df = df[df['category'] == category]

        # Category metrics
        total_rev = cat_df['total_amount'].sum()
        total_rev_pct = total_rev / df['total_amount'].sum() * 100
        transactions = len(cat_df)
        unique_customers = cat_df['customer_id'].nunique()

        # YoY growth
        cat_2022 = df[(df['category'] == category) & (df['year'] == 2022)]['total_amount'].sum()
        cat_2023 = df[(df['category'] == category) & (df['year'] == 2023)]['total_amount'].sum()
        yoy_growth = ((cat_2023 - cat_2022) / cat_2022 * 100) if cat_2022 > 0 else 0

        # Sub-categories
        subcats = cat_df.groupby('sub_category')['total_amount'].sum().sort_values(ascending=False)

        # Top brands
        top_brands = cat_df.groupby('brand')['total_amount'].sum().nlargest(5)

        # Strategic positioning
        if yoy_growth > 5:
            status = "GROWING - Expand and invest"
        elif yoy_growth > 0:
            status = "STABLE - Maintain market share"
        else:
            status = "DECLINING - Intervention needed"

        category_md += f"""## {category}

### Overview
- **Total Revenue**: ${total_rev:,.2f} ({total_rev_pct:.1f}% of total)
- **YoY Growth**: {yoy_growth:.1f}%
- **Transactions**: {transactions:,}
- **Unique Customers**: {unique_customers:,}
- **Strategic Status**: {status}

### Sub-Category Breakdown
"""
        for subcat, rev in subcats.items():
            subcat_pct = rev / total_rev * 100
            category_md += f"- **{subcat}**: ${rev:,.2f} ({subcat_pct:.1f}% of category)\n"

        category_md += "\n### Top 5 Brands\n"
        for brand, rev in top_brands.items():
            category_md += f"- {brand}: ${rev:,.2f}\n"

        category_md += "\n---\n\n"

    category_md_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/category_deep_dive_all.md'
    with open(category_md_path, 'w') as f:
        f.write(category_md)
    print(f"✓ Category deep-dive saved: {category_md_path}")

    # ========================================================================
    # 5. REGIONAL MARKET ANALYSIS
    # ========================================================================
    print("\n5. Regional Market Analysis (All regions)...")

    regional_md = f"""# Regional Market Analysis
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

    for region in df['store_region'].unique():
        reg_df = df[df['store_region'] == region]

        # Regional metrics
        total_rev = reg_df['total_amount'].sum()
        total_rev_pct = total_rev / df['total_amount'].sum() * 100
        store_count = reg_df['store_id'].nunique()
        customer_count = reg_df['customer_id'].nunique()
        revenue_per_store = total_rev / store_count

        # YoY growth
        reg_2022 = df[(df['store_region'] == region) & (df['year'] == 2022)]['total_amount'].sum()
        reg_2023 = df[(df['store_region'] == region) & (df['year'] == 2023)]['total_amount'].sum()
        yoy_growth = ((reg_2023 - reg_2022) / reg_2022 * 100) if reg_2022 > 0 else 0

        # Store performance distribution
        store_perf = reg_df.groupby('store_id')['total_amount'].sum()
        top_store_rev = store_perf.max()
        bottom_store_rev = store_perf.min()

        # Top categories in region
        top_categories = reg_df.groupby('category')['total_amount'].sum().nlargest(5)

        # Strategic assessment
        if revenue_per_store > df.groupby('store_region').apply(lambda x: x['total_amount'].sum() / x['store_id'].nunique()).median():
            market_position = "STRONG - High revenue per store"
        else:
            market_position = "MODERATE - Room for optimization"

        if yoy_growth > 3:
            growth_status = "EXPANDING"
        elif yoy_growth > -2:
            growth_status = "STABLE"
        else:
            growth_status = "CONTRACTING"

        regional_md += f"""## {region} Region

### Market Overview
- **Total Revenue**: ${total_rev:,.2f} ({total_rev_pct:.1f}% of company)
- **Store Count**: {store_count}
- **Customer Base**: {customer_count:,}
- **Revenue per Store**: ${revenue_per_store:,.2f}
- **YoY Growth**: {yoy_growth:.1f}%

### Market Position
- **Competitive Position**: {market_position}
- **Growth Status**: {growth_status}
- **Store Performance Range**: ${bottom_store_rev:,.0f} - ${top_store_rev:,.0f}

### Top 5 Categories
"""
        for cat, rev in top_categories.items():
            category_md += f"- {cat}: ${rev:,.2f}\n"

        # Strategic recommendations
        if yoy_growth > 5 and revenue_per_store > df.groupby('store_region').apply(lambda x: x['total_amount'].sum() / x['store_id'].nunique()).median():
            recommendation = "🚀 EXPAND AGGRESSIVELY - Open 3-5 new stores, high growth + strong performance"
        elif yoy_growth > 0:
            recommendation = "📈 SELECTIVE EXPANSION - Open 1-2 stores in underserved areas"
        elif yoy_growth < -5:
            recommendation = "⚠️ OPTIMIZE - Focus on improving existing stores before expansion"
        else:
            recommendation = "🔄 MAINTAIN - Steady state, focus on operational efficiency"

        regional_md += f"\n### Strategic Recommendation\n{recommendation}\n\n---\n\n"

    regional_md_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/regional_market_analysis.md'
    with open(regional_md_path, 'w') as f:
        f.write(regional_md)
    print(f"✓ Regional market analysis saved: {regional_md_path}")

    # ========================================================================
    # COMPLETION
    # ========================================================================
    print()
    print("=" * 80)
    print("✅ GRANULAR DEEP-DIVE INSIGHTS COMPLETE!")
    print("=" * 80)
    print(f"Store Insights: Top 50 + Bottom 50 analyzed")
    print(f"Product Insights: Top 100 analyzed")
    print(f"Customer Segments: {len(segment_insights)} segments profiled")
    print(f"Categories: {df['category'].nunique()} categories analyzed")
    print(f"Regions: {df['store_region'].nunique()} regions analyzed")
    print(f"Files Created: 6 (2 store CSVs, 1 product CSV, 3 MDs)")

if __name__ == "__main__":
    granular_insights()
