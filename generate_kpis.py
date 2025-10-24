import pandas as pd
import numpy as np
from datetime import datetime

print("Loading grocery dataset...")
# Load the dataset in chunks to handle large file
chunk_size = 100000
chunks = []

for chunk in pd.read_csv('grocery_dataset.csv', chunksize=chunk_size):
    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)
print(f"Loaded {len(df)} records")

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['month'] = df['timestamp'].dt.to_period('M')
df['week'] = df['timestamp'].dt.to_period('W')

# ===== OVERALL BUSINESS KPIs =====
print("\nCalculating Overall Business KPIs...")

overall_kpis = pd.DataFrame({
    'KPI_Category': ['Overall Business'],
    'Total_Revenue': [df['total_amount'].sum()],
    'Total_Transactions': [len(df)],
    'Total_Items_Sold': [df['quantity'].sum()],
    'Average_Transaction_Value': [df.groupby('transaction_id')['total_amount'].sum().mean()],
    'Average_Basket_Size': [df['basket_size'].mean()],
    'Average_Items_Per_Transaction': [df.groupby('transaction_id')['quantity'].sum().mean()],
    'Total_Discount_Given': [df.apply(lambda x: x['unit_price'] * x['quantity'] * x['discount_percentage'] / 100, axis=1).sum()],
    'Average_Discount_Percentage': [df['discount_percentage'].mean()],
    'Unique_Customers': [df['customer_id'].nunique()],
    'Unique_Products': [df['product_id'].nunique()]
})

# ===== STORE PERFORMANCE KPIs =====
print("Calculating Store Performance KPIs...")

store_kpis = df.groupby('store_id').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'quantity': 'sum',
    'customer_id': 'nunique',
    'discount_percentage': 'mean',
    'basket_size': 'mean'
}).round(2)

store_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions',
                       'Total_Items_Sold', 'Unique_Customers', 'Avg_Discount_%', 'Avg_Basket_Size']
store_kpis = store_kpis.reset_index()
store_kpis.insert(1, 'KPI_Category', 'Store Performance')

# Add store region and type
store_info = df.groupby('store_id')[['store_region', 'store_type']].first().reset_index()
store_kpis = store_kpis.merge(store_info, on='store_id')

# ===== CATEGORY PERFORMANCE KPIs =====
print("Calculating Category Performance KPIs...")

category_kpis = df.groupby('category').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum',
    'discount_percentage': 'mean',
    'customer_id': 'nunique'
}).round(2)

category_kpis.columns = ['Total_Revenue', 'Total_Transactions', 'Total_Items_Sold',
                          'Avg_Discount_%', 'Unique_Customers']
category_kpis = category_kpis.reset_index()
category_kpis.insert(1, 'KPI_Category', 'Category Performance')
category_kpis = category_kpis.sort_values('Total_Revenue', ascending=False)

# ===== PRODUCT PERFORMANCE KPIs (Top 50) =====
print("Calculating Product Performance KPIs...")

product_kpis = df.groupby(['product_id', 'product_name', 'category']).agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum',
    'discount_percentage': 'mean'
}).round(2)

product_kpis.columns = ['Total_Revenue', 'Total_Transactions', 'Total_Quantity_Sold', 'Avg_Discount_%']
product_kpis = product_kpis.reset_index()
product_kpis.insert(3, 'KPI_Category', 'Product Performance')
product_kpis = product_kpis.sort_values('Total_Revenue', ascending=False).head(50)

# ===== CUSTOMER SEGMENT KPIs =====
print("Calculating Customer Segment KPIs...")

customer_segment_kpis = df.groupby('customer_type').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'customer_id': 'nunique',
    'loyalty_points_earned': 'sum',
    'basket_size': 'mean'
}).round(2)

customer_segment_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions',
                                   'Unique_Customers', 'Total_Loyalty_Points_Earned', 'Avg_Basket_Size']
customer_segment_kpis = customer_segment_kpis.reset_index()
customer_segment_kpis.insert(1, 'KPI_Category', 'Customer Segment')

# ===== TIME-BASED KPIs =====
print("Calculating Time-based KPIs...")

# Daily KPIs
daily_kpis = df.groupby('date').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum'
}).round(2)
daily_kpis.columns = ['Total_Revenue', 'Total_Transactions', 'Total_Items_Sold']
daily_kpis = daily_kpis.reset_index()
daily_kpis.insert(1, 'KPI_Category', 'Daily Performance')

# Weekly KPIs
weekly_kpis = df.groupby('week').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum'
}).round(2)
weekly_kpis.columns = ['Total_Revenue', 'Total_Transactions', 'Total_Items_Sold']
weekly_kpis = weekly_kpis.reset_index()
weekly_kpis['week'] = weekly_kpis['week'].astype(str)
weekly_kpis.insert(1, 'KPI_Category', 'Weekly Performance')

# Monthly KPIs
monthly_kpis = df.groupby('month').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum',
    'customer_id': 'nunique'
}).round(2)
monthly_kpis.columns = ['Total_Revenue', 'Total_Transactions', 'Total_Items_Sold', 'Unique_Customers']
monthly_kpis = monthly_kpis.reset_index()
monthly_kpis['month'] = monthly_kpis['month'].astype(str)
monthly_kpis.insert(1, 'KPI_Category', 'Monthly Performance')

# ===== PAYMENT METHOD KPIs =====
print("Calculating Payment Method KPIs...")

payment_kpis = df.groupby('payment_method').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count'
}).round(2)
payment_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions']
payment_kpis = payment_kpis.reset_index()
payment_kpis.insert(1, 'KPI_Category', 'Payment Method')

# ===== TIME SLOT KPIs =====
print("Calculating Time Slot KPIs...")

timeslot_kpis = df.groupby('time_slot').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'basket_size': 'mean'
}).round(2)
timeslot_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions', 'Avg_Basket_Size']
timeslot_kpis = timeslot_kpis.reset_index()
timeslot_kpis.insert(1, 'KPI_Category', 'Time Slot Performance')

# ===== DELIVERY METHOD KPIs =====
print("Calculating Delivery Method KPIs...")

delivery_kpis = df.groupby('delivery_method').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'basket_size': 'mean'
}).round(2)
delivery_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions', 'Avg_Basket_Size']
delivery_kpis = delivery_kpis.reset_index()
delivery_kpis.insert(1, 'KPI_Category', 'Delivery Method')

# ===== WEEKEND vs WEEKDAY KPIs =====
print("Calculating Weekend vs Weekday KPIs...")

weekend_kpis = df.groupby('is_weekend').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'basket_size': 'mean'
}).round(2)
weekend_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions', 'Avg_Basket_Size']
weekend_kpis = weekend_kpis.reset_index()
weekend_kpis['is_weekend'] = weekend_kpis['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
weekend_kpis.rename(columns={'is_weekend': 'day_type'}, inplace=True)
weekend_kpis.insert(1, 'KPI_Category', 'Weekend vs Weekday')

# ===== AGE GROUP KPIs =====
print("Calculating Age Group KPIs...")

age_kpis = df.groupby('age_group').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'customer_id': 'nunique',
    'basket_size': 'mean'
}).round(2)
age_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions',
                     'Unique_Customers', 'Avg_Basket_Size']
age_kpis = age_kpis.reset_index()
age_kpis.insert(1, 'KPI_Category', 'Age Group')

# ===== GENDER KPIs =====
print("Calculating Gender KPIs...")

gender_kpis = df.groupby('gender').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'customer_id': 'nunique',
    'basket_size': 'mean'
}).round(2)
gender_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions',
                        'Unique_Customers', 'Avg_Basket_Size']
gender_kpis = gender_kpis.reset_index()
gender_kpis.insert(1, 'KPI_Category', 'Gender')

# ===== SEASONAL KPIs =====
print("Calculating Seasonal KPIs...")

season_kpis = df.groupby('season').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'basket_size': 'mean'
}).round(2)
season_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions', 'Avg_Basket_Size']
season_kpis = season_kpis.reset_index()
season_kpis.insert(1, 'KPI_Category', 'Seasonal Performance')

# ===== BRAND PERFORMANCE KPIs (Top 30) =====
print("Calculating Brand Performance KPIs...")

brand_kpis = df.groupby('brand').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum'
}).round(2)
brand_kpis.columns = ['Total_Revenue', 'Total_Transactions', 'Total_Quantity_Sold']
brand_kpis = brand_kpis.reset_index()
brand_kpis.insert(1, 'KPI_Category', 'Brand Performance')
brand_kpis = brand_kpis.sort_values('Total_Revenue', ascending=False).head(30)

# ===== ORGANIC vs NON-ORGANIC KPIs =====
print("Calculating Organic vs Non-Organic KPIs...")

organic_kpis = df.groupby('is_organic').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'quantity': 'sum'
}).round(2)
organic_kpis.columns = ['Total_Revenue', 'Avg_Transaction_Value', 'Total_Transactions', 'Total_Quantity_Sold']
organic_kpis = organic_kpis.reset_index()
organic_kpis['is_organic'] = organic_kpis['is_organic'].map({True: 'Organic', False: 'Non-Organic'})
organic_kpis.rename(columns={'is_organic': 'product_type'}, inplace=True)
organic_kpis.insert(1, 'KPI_Category', 'Organic vs Non-Organic')

# ===== EMPLOYEE PERFORMANCE KPIs (Top 50) =====
print("Calculating Employee Performance KPIs...")

employee_kpis = df.groupby('employee_id').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'checkout_duration_sec': 'mean'
}).round(2)
employee_kpis.columns = ['Total_Revenue', 'Total_Transactions', 'Avg_Checkout_Duration_Sec']
employee_kpis = employee_kpis.reset_index()
employee_kpis.insert(1, 'KPI_Category', 'Employee Performance')
employee_kpis = employee_kpis.sort_values('Total_Revenue', ascending=False).head(50)

# ===== SAVE ALL KPIs TO SEPARATE CSV FILES =====
print("\n\nSaving KPIs to CSV files...")

overall_kpis.to_csv('kpi_overall_business.csv', index=False)
print("✓ Saved: kpi_overall_business.csv")

store_kpis.to_csv('kpi_store_performance.csv', index=False)
print("✓ Saved: kpi_store_performance.csv")

category_kpis.to_csv('kpi_category_performance.csv', index=False)
print("✓ Saved: kpi_category_performance.csv")

product_kpis.to_csv('kpi_product_performance.csv', index=False)
print("✓ Saved: kpi_product_performance.csv")

customer_segment_kpis.to_csv('kpi_customer_segment.csv', index=False)
print("✓ Saved: kpi_customer_segment.csv")

daily_kpis.to_csv('kpi_daily_performance.csv', index=False)
print("✓ Saved: kpi_daily_performance.csv")

weekly_kpis.to_csv('kpi_weekly_performance.csv', index=False)
print("✓ Saved: kpi_weekly_performance.csv")

monthly_kpis.to_csv('kpi_monthly_performance.csv', index=False)
print("✓ Saved: kpi_monthly_performance.csv")

payment_kpis.to_csv('kpi_payment_method.csv', index=False)
print("✓ Saved: kpi_payment_method.csv")

timeslot_kpis.to_csv('kpi_time_slot.csv', index=False)
print("✓ Saved: kpi_time_slot.csv")

delivery_kpis.to_csv('kpi_delivery_method.csv', index=False)
print("✓ Saved: kpi_delivery_method.csv")

weekend_kpis.to_csv('kpi_weekend_weekday.csv', index=False)
print("✓ Saved: kpi_weekend_weekday.csv")

age_kpis.to_csv('kpi_age_group.csv', index=False)
print("✓ Saved: kpi_age_group.csv")

gender_kpis.to_csv('kpi_gender.csv', index=False)
print("✓ Saved: kpi_gender.csv")

season_kpis.to_csv('kpi_seasonal.csv', index=False)
print("✓ Saved: kpi_seasonal.csv")

brand_kpis.to_csv('kpi_brand_performance.csv', index=False)
print("✓ Saved: kpi_brand_performance.csv")

organic_kpis.to_csv('kpi_organic_vs_nonorganic.csv', index=False)
print("✓ Saved: kpi_organic_vs_nonorganic.csv")

employee_kpis.to_csv('kpi_employee_performance.csv', index=False)
print("✓ Saved: kpi_employee_performance.csv")

# ===== CREATE MASTER SUMMARY KPI DASHBOARD =====
print("\n\nCreating Master KPI Dashboard...")

# Create a summary dashboard with key metrics
dashboard_data = {
    'Metric': [
        'Total Revenue',
        'Total Transactions',
        'Total Items Sold',
        'Average Transaction Value',
        'Average Basket Size',
        'Total Unique Customers',
        'Total Unique Products',
        'Average Discount %',
        'Top Store (by Revenue)',
        'Top Category (by Revenue)',
        'Top Product (by Revenue)',
        'Most Popular Payment Method',
        'Peak Time Slot',
        'Home Delivery %',
        'Weekend Sales %',
        'Organic Product Sales %'
    ],
    'Value': [
        f"${overall_kpis['Total_Revenue'].iloc[0]:,.2f}",
        f"{overall_kpis['Total_Transactions'].iloc[0]:,}",
        f"{overall_kpis['Total_Items_Sold'].iloc[0]:,}",
        f"${overall_kpis['Average_Transaction_Value'].iloc[0]:,.2f}",
        f"{overall_kpis['Average_Basket_Size'].iloc[0]:.2f}",
        f"{overall_kpis['Unique_Customers'].iloc[0]:,}",
        f"{overall_kpis['Unique_Products'].iloc[0]:,}",
        f"{overall_kpis['Average_Discount_Percentage'].iloc[0]:.2f}%",
        f"{store_kpis.loc[store_kpis['Total_Revenue'].idxmax(), 'store_id']} (${store_kpis['Total_Revenue'].max():,.2f})",
        f"{category_kpis.iloc[0]['category']} (${category_kpis.iloc[0]['Total_Revenue']:,.2f})",
        f"{product_kpis.iloc[0]['product_name']} (${product_kpis.iloc[0]['Total_Revenue']:,.2f})",
        f"{payment_kpis.loc[payment_kpis['Total_Transactions'].idxmax(), 'payment_method']} ({payment_kpis['Total_Transactions'].max():,} txns)",
        f"{timeslot_kpis.loc[timeslot_kpis['Total_Transactions'].idxmax(), 'time_slot']} ({timeslot_kpis['Total_Transactions'].max():,} txns)",
        f"{(df['delivery_method'].value_counts(normalize=True).get('Home Delivery', 0) * 100):.1f}%",
        f"{(df['is_weekend'].sum() / len(df) * 100):.1f}%",
        f"{(df['is_organic'].sum() / len(df) * 100):.1f}%"
    ]
}

dashboard_df = pd.DataFrame(dashboard_data)
dashboard_df.to_csv('kpi_master_dashboard.csv', index=False)
print("✓ Saved: kpi_master_dashboard.csv")

print("\n" + "="*70)
print("ALL KPIs GENERATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated KPI Files:")
print("1.  kpi_master_dashboard.csv - Executive summary with key metrics")
print("2.  kpi_overall_business.csv - Overall business KPIs")
print("3.  kpi_store_performance.csv - Store-wise performance")
print("4.  kpi_category_performance.csv - Category-wise performance")
print("5.  kpi_product_performance.csv - Top 50 products")
print("6.  kpi_customer_segment.csv - Customer segment analysis")
print("7.  kpi_daily_performance.csv - Daily performance trends")
print("8.  kpi_weekly_performance.csv - Weekly performance trends")
print("9.  kpi_monthly_performance.csv - Monthly performance trends")
print("10. kpi_payment_method.csv - Payment method analysis")
print("11. kpi_time_slot.csv - Time slot performance")
print("12. kpi_delivery_method.csv - Delivery method analysis")
print("13. kpi_weekend_weekday.csv - Weekend vs Weekday comparison")
print("14. kpi_age_group.csv - Age group analysis")
print("15. kpi_gender.csv - Gender-based analysis")
print("16. kpi_seasonal.csv - Seasonal performance")
print("17. kpi_brand_performance.csv - Top 30 brands")
print("18. kpi_organic_vs_nonorganic.csv - Organic vs Non-Organic comparison")
print("19. kpi_employee_performance.csv - Top 50 employee performance")
print("="*70)
