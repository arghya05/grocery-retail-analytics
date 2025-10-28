#!/usr/bin/env python3
"""
Generate all KPI CSV files from USD-converted grocery dataset
"""
import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 80)
print("KPI GENERATION FOR CEO FOLDER (USD VALUES)")
print("=" * 80)

# Configuration
DATA_FILE = '/Users/arghya.mukherjee/Downloads/cursor/sd/grocery_dataset_usd.csv'
OUTPUT_DIR = '/Users/arghya.mukherjee/Downloads/cursor/sd/ceo_new'

print(f"\nReading dataset: {DATA_FILE}")
print("This may take a moment...")

# Read the USD converted dataset
df = pd.read_csv(DATA_FILE)

print(f"✓ Loaded {len(df):,} transactions")
print(f"✓ Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"✓ Total revenue: ${df['total_amount'].sum():,.2f}")

# Create output directory
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. KPI: Overall Business Performance
# ============================================================================
print("\n[1/19] Generating kpi_overall_business.csv...")
overall_kpi = pd.DataFrame({
    'metric': [
        'Total Revenue',
        'Total Transactions',
        'Unique Customers',
        'Average Transaction Value',
        'Total Products Sold',
        'Average Basket Size',
        'Total Stores',
        'Average Daily Revenue',
        'Average Daily Transactions',
        'Revenue per Customer'
    ],
    'value': [
        f"${df['total_amount'].sum():,.2f}",
        f"{len(df):,}",
        f"{df['customer_id'].nunique():,}",
        f"${df['total_amount'].mean():.2f}",
        f"{df['quantity'].sum():,}",
        f"{df['basket_size'].mean():.2f}",
        f"{df['store_id'].nunique()}",
        f"${df.groupby(df['timestamp'].str[:10])['total_amount'].sum().mean():,.2f}",
        f"{df.groupby(df['timestamp'].str[:10]).size().mean():.0f}",
        f"${df.groupby('customer_id')['total_amount'].sum().mean():.2f}"
    ]
})
overall_kpi.to_csv(f"{OUTPUT_DIR}/kpi_overall_business.csv", index=False)
print(f"   ✓ Total Revenue: ${df['total_amount'].sum():,.2f}")

# ============================================================================
# 2. KPI: Store Performance
# ============================================================================
print("[2/19] Generating kpi_store_performance.csv...")
store_kpi = df.groupby(['store_id', 'store_region', 'store_type']).agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'quantity': 'sum',
    'basket_size': 'mean'
}).round(2)
store_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                      'unique_customers', 'total_items_sold', 'avg_basket_size']
store_kpi = store_kpi.reset_index().sort_values('total_revenue', ascending=False)
store_kpi.to_csv(f"{OUTPUT_DIR}/kpi_store_performance.csv", index=False)
print(f"   ✓ Stores analyzed: {len(store_kpi)}")

# ============================================================================
# 3. KPI: Category Performance
# ============================================================================
print("[3/19] Generating kpi_category_performance.csv...")
category_kpi = df.groupby('category').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'quantity': 'sum',
    'discount_percentage': 'mean',
    'customer_id': 'nunique'
}).round(2)
category_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                        'total_quantity', 'avg_discount_pct', 'unique_customers']
category_kpi['revenue_share_pct'] = (category_kpi['total_revenue'] / category_kpi['total_revenue'].sum() * 100).round(2)
category_kpi = category_kpi.reset_index().sort_values('total_revenue', ascending=False)
category_kpi.to_csv(f"{OUTPUT_DIR}/kpi_category_performance.csv", index=False)
print(f"   ✓ Categories: {len(category_kpi)}")

# ============================================================================
# 4. KPI: Product Performance
# ============================================================================
print("[4/19] Generating kpi_product_performance.csv...")
product_kpi = df.groupby(['product_id', 'product_name', 'category', 'brand']).agg({
    'total_amount': ['sum', 'mean', 'count'],
    'quantity': 'sum',
    'discount_percentage': 'mean'
}).round(2)
product_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                       'total_quantity_sold', 'avg_discount_pct']
product_kpi = product_kpi.reset_index().sort_values('total_revenue', ascending=False)
product_kpi.to_csv(f"{OUTPUT_DIR}/kpi_product_performance.csv", index=False)
print(f"   ✓ Products: {len(product_kpi)}")

# ============================================================================
# 5. KPI: Customer Segment Performance
# ============================================================================
print("[5/19] Generating kpi_customer_segment.csv...")
customer_kpi = df.groupby('customer_type').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'basket_size': 'mean',
    'quantity': 'sum'
}).round(2)
customer_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                        'unique_customers', 'avg_basket_size', 'total_items']
customer_kpi['revenue_share_pct'] = (customer_kpi['total_revenue'] / customer_kpi['total_revenue'].sum() * 100).round(2)
customer_kpi = customer_kpi.reset_index().sort_values('total_revenue', ascending=False)
customer_kpi.to_csv(f"{OUTPUT_DIR}/kpi_customer_segment.csv", index=False)
print(f"   ✓ Segments: {len(customer_kpi)}")

# ============================================================================
# 6. KPI: Monthly Performance
# ============================================================================
print("[6/19] Generating kpi_monthly_performance.csv...")
df['year_month'] = pd.to_datetime(df['timestamp']).dt.to_period('M').astype(str)
monthly_kpi = df.groupby('year_month').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'basket_size': 'mean'
}).round(2)
monthly_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                       'unique_customers', 'avg_basket_size']
monthly_kpi = monthly_kpi.reset_index().sort_values('year_month')
monthly_kpi.to_csv(f"{OUTPUT_DIR}/kpi_monthly_performance.csv", index=False)
print(f"   ✓ Months: {len(monthly_kpi)}")

# ============================================================================
# 7. KPI: Daily Performance
# ============================================================================
print("[7/19] Generating kpi_daily_performance.csv...")
df['date'] = pd.to_datetime(df['timestamp']).dt.date.astype(str)
daily_kpi = df.groupby('date').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
}).round(2)
daily_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions', 'unique_customers']
daily_kpi = daily_kpi.reset_index().sort_values('date')
daily_kpi.to_csv(f"{OUTPUT_DIR}/kpi_daily_performance.csv", index=False)
print(f"   ✓ Days: {len(daily_kpi)}")

# ============================================================================
# 8. KPI: Weekly Performance
# ============================================================================
print("[8/19] Generating kpi_weekly_performance.csv...")
df['year_week'] = pd.to_datetime(df['timestamp']).dt.isocalendar().week.astype(str) + '-' + pd.to_datetime(df['timestamp']).dt.isocalendar().year.astype(str)
weekly_kpi = df.groupby('year_week').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
}).round(2)
weekly_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions', 'unique_customers']
weekly_kpi = weekly_kpi.reset_index()
weekly_kpi.to_csv(f"{OUTPUT_DIR}/kpi_weekly_performance.csv", index=False)
print(f"   ✓ Weeks: {len(weekly_kpi)}")

# ============================================================================
# 9. KPI: Age Group Performance
# ============================================================================
print("[9/19] Generating kpi_age_group.csv...")
age_kpi = df.groupby('age_group').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'basket_size': 'mean'
}).round(2)
age_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                   'unique_customers', 'avg_basket_size']
age_kpi['revenue_share_pct'] = (age_kpi['total_revenue'] / age_kpi['total_revenue'].sum() * 100).round(2)
age_kpi = age_kpi.reset_index().sort_values('total_revenue', ascending=False)
age_kpi.to_csv(f"{OUTPUT_DIR}/kpi_age_group.csv", index=False)
print(f"   ✓ Age groups: {len(age_kpi)}")

# ============================================================================
# 10. KPI: Gender Performance
# ============================================================================
print("[10/19] Generating kpi_gender.csv...")
gender_kpi = df.groupby('gender').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'basket_size': 'mean'
}).round(2)
gender_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                      'unique_customers', 'avg_basket_size']
gender_kpi['revenue_share_pct'] = (gender_kpi['total_revenue'] / gender_kpi['total_revenue'].sum() * 100).round(2)
gender_kpi = gender_kpi.reset_index()
gender_kpi.to_csv(f"{OUTPUT_DIR}/kpi_gender.csv", index=False)
print(f"   ✓ Genders: {len(gender_kpi)}")

# ============================================================================
# 11. KPI: Payment Method
# ============================================================================
print("[11/19] Generating kpi_payment_method.csv...")
payment_kpi = df.groupby('payment_method').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
}).round(2)
payment_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions', 'unique_customers']
payment_kpi['transaction_share_pct'] = (payment_kpi['total_transactions'] / payment_kpi['total_transactions'].sum() * 100).round(2)
payment_kpi = payment_kpi.reset_index().sort_values('total_revenue', ascending=False)
payment_kpi.to_csv(f"{OUTPUT_DIR}/kpi_payment_method.csv", index=False)
print(f"   ✓ Payment methods: {len(payment_kpi)}")

# ============================================================================
# 12. KPI: Time Slot Performance
# ============================================================================
print("[12/19] Generating kpi_time_slot.csv...")
timeslot_kpi = df.groupby('time_slot').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'basket_size': 'mean'
}).round(2)
timeslot_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                        'unique_customers', 'avg_basket_size']
timeslot_kpi['transaction_share_pct'] = (timeslot_kpi['total_transactions'] / timeslot_kpi['total_transactions'].sum() * 100).round(2)
timeslot_kpi = timeslot_kpi.reset_index().sort_values('total_revenue', ascending=False)
timeslot_kpi.to_csv(f"{OUTPUT_DIR}/kpi_time_slot.csv", index=False)
print(f"   ✓ Time slots: {len(timeslot_kpi)}")

# ============================================================================
# 13. KPI: Seasonal Performance
# ============================================================================
print("[13/19] Generating kpi_seasonal.csv...")
seasonal_kpi = df.groupby('season').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'basket_size': 'mean'
}).round(2)
seasonal_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                        'unique_customers', 'avg_basket_size']
seasonal_kpi['revenue_share_pct'] = (seasonal_kpi['total_revenue'] / seasonal_kpi['total_revenue'].sum() * 100).round(2)
seasonal_kpi = seasonal_kpi.reset_index().sort_values('total_revenue', ascending=False)
seasonal_kpi.to_csv(f"{OUTPUT_DIR}/kpi_seasonal.csv", index=False)
print(f"   ✓ Seasons: {len(seasonal_kpi)}")

# ============================================================================
# 14. KPI: Weekend vs Weekday
# ============================================================================
print("[14/19] Generating kpi_weekend_weekday.csv...")
weekend_kpi = df.groupby('is_weekend').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'basket_size': 'mean'
}).round(2)
weekend_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                       'unique_customers', 'avg_basket_size']
weekend_kpi['period'] = weekend_kpi.index.map({True: 'Weekend', False: 'Weekday'})
weekend_kpi = weekend_kpi.reset_index(drop=True)
weekend_kpi = weekend_kpi[['period', 'total_revenue', 'avg_transaction_value', 'total_transactions',
                            'unique_customers', 'avg_basket_size']]
weekend_kpi.to_csv(f"{OUTPUT_DIR}/kpi_weekend_weekday.csv", index=False)
print(f"   ✓ Weekend/Weekday split generated")

# ============================================================================
# 15. KPI: Delivery Method
# ============================================================================
print("[15/19] Generating kpi_delivery_method.csv...")
delivery_kpi = df.groupby('delivery_method').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
}).round(2)
delivery_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions', 'unique_customers']
delivery_kpi['transaction_share_pct'] = (delivery_kpi['total_transactions'] / delivery_kpi['total_transactions'].sum() * 100).round(2)
delivery_kpi = delivery_kpi.reset_index().sort_values('total_revenue', ascending=False)
delivery_kpi.to_csv(f"{OUTPUT_DIR}/kpi_delivery_method.csv", index=False)
print(f"   ✓ Delivery methods: {len(delivery_kpi)}")

# ============================================================================
# 16. KPI: Brand Performance
# ============================================================================
print("[16/19] Generating kpi_brand_performance.csv...")
brand_kpi = df.groupby('brand').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'quantity': 'sum',
    'discount_percentage': 'mean'
}).round(2)
brand_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                     'total_quantity', 'avg_discount_pct']
brand_kpi = brand_kpi.reset_index().sort_values('total_revenue', ascending=False)
brand_kpi.to_csv(f"{OUTPUT_DIR}/kpi_brand_performance.csv", index=False)
print(f"   ✓ Brands: {len(brand_kpi)}")

# ============================================================================
# 17. KPI: Organic vs Non-Organic
# ============================================================================
print("[17/19] Generating kpi_organic_vs_nonorganic.csv...")
organic_kpi = df.groupby('is_organic').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
}).round(2)
organic_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions', 'unique_customers']
organic_kpi['product_type'] = organic_kpi.index.map({True: 'Organic', False: 'Non-Organic'})
organic_kpi = organic_kpi.reset_index(drop=True)
organic_kpi = organic_kpi[['product_type', 'total_revenue', 'avg_transaction_value',
                            'total_transactions', 'unique_customers']]
organic_kpi.to_csv(f"{OUTPUT_DIR}/kpi_organic_vs_nonorganic.csv", index=False)
print(f"   ✓ Organic vs Non-Organic generated")

# ============================================================================
# 18. KPI: Employee Performance
# ============================================================================
print("[18/19] Generating kpi_employee_performance.csv...")
employee_kpi = df.groupby('employee_id').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'checkout_duration_sec': 'mean'
}).round(2)
employee_kpi.columns = ['total_revenue', 'avg_transaction_value', 'total_transactions',
                        'unique_customers', 'avg_checkout_time_sec']
employee_kpi = employee_kpi.reset_index().sort_values('total_revenue', ascending=False)
employee_kpi.to_csv(f"{OUTPUT_DIR}/kpi_employee_performance.csv", index=False)
print(f"   ✓ Employees: {len(employee_kpi)}")

# ============================================================================
# 19. KPI: Master Dashboard (Summary)
# ============================================================================
print("[19/19] Generating kpi_master_dashboard.csv...")

# Calculate some key metrics
total_revenue = df['total_amount'].sum()
total_transactions = len(df)
unique_customers = df['customer_id'].nunique()
avg_transaction = df['total_amount'].mean()
total_stores = df['store_id'].nunique()

# Promotion analysis
promo_txns = df[df['discount_percentage'] > 0]
no_promo_txns = df[df['discount_percentage'] == 0]
promo_avg = promo_txns['total_amount'].mean() if len(promo_txns) > 0 else 0
no_promo_avg = no_promo_txns['total_amount'].mean() if len(no_promo_txns) > 0 else 0

# Top performers
top_store = df.groupby('store_id')['total_amount'].sum().idxmax()
top_product = df.groupby('product_name')['total_amount'].sum().idxmax()
top_category = df.groupby('category')['total_amount'].sum().idxmax()

master_dashboard = pd.DataFrame({
    'kpi_category': [
        'Revenue', 'Revenue', 'Revenue', 'Revenue', 'Revenue',
        'Transactions', 'Transactions', 'Transactions',
        'Customers', 'Customers', 'Customers',
        'Operations', 'Operations', 'Operations',
        'Promotions', 'Promotions', 'Promotions',
        'Top Performers', 'Top Performers', 'Top Performers'
    ],
    'kpi_name': [
        'Total Revenue', 'Daily Revenue', 'Revenue per Store', 'Revenue per Customer', 'Avg Transaction Value',
        'Total Transactions', 'Daily Transactions', 'Avg Basket Size',
        'Unique Customers', 'Customer Retention %', 'Avg Transactions per Customer',
        'Total Stores', 'Digital Payment %', 'Avg Checkout Time',
        'Transactions with Promos %', 'Avg Value (With Promo)', 'Avg Value (No Promo)',
        'Top Store', 'Top Product', 'Top Category'
    ],
    'value': [
        f"${total_revenue:,.2f}",
        f"${df.groupby(df['timestamp'].str[:10])['total_amount'].sum().mean():,.2f}",
        f"${total_revenue / total_stores:,.2f}",
        f"${df.groupby('customer_id')['total_amount'].sum().mean():.2f}",
        f"${avg_transaction:.2f}",
        f"{total_transactions:,}",
        f"{df.groupby(df['timestamp'].str[:10]).size().mean():.0f}",
        f"{df['basket_size'].mean():.2f}",
        f"{unique_customers:,}",
        f"{(df[df['customer_type'] == 'Regular']['customer_id'].nunique() / unique_customers * 100):.1f}%",
        f"{total_transactions / unique_customers:.2f}",
        f"{total_stores}",
        f"{((df['payment_method'] != 'Cash').sum() / total_transactions * 100):.1f}%",
        f"{df['checkout_duration_sec'].mean():.0f} seconds",
        f"{(len(promo_txns) / total_transactions * 100):.1f}%",
        f"${promo_avg:.2f}",
        f"${no_promo_avg:.2f}",
        top_store,
        top_product,
        top_category
    ]
})
master_dashboard.to_csv(f"{OUTPUT_DIR}/kpi_master_dashboard.csv", index=False)
print(f"   ✓ Master dashboard created with 20 key metrics")

# ============================================================================
# Additional: Store Manager Dashboard
# ============================================================================
print("\n[BONUS] Generating store_manager_kpi_dashboard.csv...")
store_manager_summary = pd.DataFrame({
    'store_id': df.groupby('store_id')['total_amount'].sum().index,
    'total_revenue': df.groupby('store_id')['total_amount'].sum().values.round(2),
    'total_transactions': df.groupby('store_id').size().values,
    'avg_transaction_value': df.groupby('store_id')['total_amount'].mean().values.round(2),
    'unique_customers': df.groupby('store_id')['customer_id'].nunique().values,
    'top_category': df.groupby('store_id').apply(lambda x: x.groupby('category')['total_amount'].sum().idxmax()).values,
    'digital_payment_pct': df.groupby('store_id').apply(lambda x: ((x['payment_method'] != 'Cash').sum() / len(x) * 100)).values.round(1)
})
store_manager_summary = store_manager_summary.sort_values('total_revenue', ascending=False)
store_manager_summary.to_csv(f"{OUTPUT_DIR}/store_manager_kpi_dashboard.csv", index=False)
print(f"   ✓ Store Manager dashboard created")

# ============================================================================
# Summary Report
# ============================================================================
print("\n" + "=" * 80)
print("KPI GENERATION COMPLETE!")
print("=" * 80)
print(f"\nAll KPI files generated in: {OUTPUT_DIR}")
print("\nKey Metrics (USD):")
print(f"  → Total Revenue: ${total_revenue:,.2f}")
print(f"  → Total Transactions: {total_transactions:,}")
print(f"  → Unique Customers: {unique_customers:,}")
print(f"  → Avg Transaction Value: ${avg_transaction:.2f}")
print(f"  → Total Stores: {total_stores}")
print(f"  → Revenue per Store: ${total_revenue / total_stores:,.2f}")
print("\nFiles Generated:")
print("  1. kpi_overall_business.csv")
print("  2. kpi_store_performance.csv")
print("  3. kpi_category_performance.csv")
print("  4. kpi_product_performance.csv")
print("  5. kpi_customer_segment.csv")
print("  6. kpi_monthly_performance.csv")
print("  7. kpi_daily_performance.csv")
print("  8. kpi_weekly_performance.csv")
print("  9. kpi_age_group.csv")
print("  10. kpi_gender.csv")
print("  11. kpi_payment_method.csv")
print("  12. kpi_time_slot.csv")
print("  13. kpi_seasonal.csv")
print("  14. kpi_weekend_weekday.csv")
print("  15. kpi_delivery_method.csv")
print("  16. kpi_brand_performance.csv")
print("  17. kpi_organic_vs_nonorganic.csv")
print("  18. kpi_employee_performance.csv")
print("  19. kpi_master_dashboard.csv")
print("  20. store_manager_kpi_dashboard.csv (bonus)")
print("\n" + "=" * 80)
print("Ready for CEO analysis and strategic decision-making!")
print("=" * 80)
