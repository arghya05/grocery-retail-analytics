import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print(" " * 30 + "STORE MANAGER INSIGHTS DASHBOARD")
print("=" * 100)
print("\nLoading grocery dataset...")

df = pd.read_csv('grocery_dataset.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.day_name()
df['month'] = df['timestamp'].dt.month
df['month_name'] = df['timestamp'].dt.strftime('%B')

print(f"✓ Loaded {len(df):,} transactions")
print(f"  Period: {df['timestamp'].min().date()} to {df['timestamp'].max().date()}")
print(f"  Total Revenue: ₹{df['total_amount'].sum():,.2f}")
print("\n" + "=" * 100)

# ============================================================================
# 1. SALES PERFORMANCE ANALYSIS
# ============================================================================
print("\n📊 1. SALES PERFORMANCE ANALYSIS")
print("=" * 100)

# Overall metrics
total_revenue = df['total_amount'].sum()
avg_transaction = df['total_amount'].mean()
total_transactions = len(df)
total_items_sold = df['quantity'].sum()

print(f"\n📈 KEY METRICS:")
print(f"   Total Revenue:        ₹{total_revenue:,.2f}")
print(f"   Total Transactions:   {total_transactions:,}")
print(f"   Avg Transaction:      ₹{avg_transaction:.2f}")
print(f"   Total Items Sold:     {total_items_sold:,}")
print(f"   Avg Items/Transaction: {total_items_sold/total_transactions:.2f}")

# Top performing categories
print(f"\n🏆 TOP 5 CATEGORIES BY REVENUE:")
cat_revenue = df.groupby('category').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum'
}).sort_values('total_amount', ascending=False)
cat_revenue.columns = ['Revenue', 'Transactions', 'Units']
cat_revenue['Avg_Transaction'] = cat_revenue['Revenue'] / cat_revenue['Transactions']
cat_revenue['Revenue_%'] = (cat_revenue['Revenue'] / total_revenue * 100).round(2)

for idx, (cat, row) in enumerate(cat_revenue.head().iterrows(), 1):
    print(f"   {idx}. {cat:25} ₹{row['Revenue']:12,.2f} ({row['Revenue_%']:5.2f}%) - {row['Transactions']:,} trans")

# Top products
print(f"\n💰 TOP 10 PRODUCTS BY REVENUE:")
prod_revenue = df.groupby(['product_name', 'category']).agg({
    'total_amount': 'sum',
    'quantity': 'sum',
    'transaction_id': 'count'
}).sort_values('total_amount', ascending=False)

for idx, ((prod, cat), row) in enumerate(prod_revenue.head(10).iterrows(), 1):
    rev_pct = (row['total_amount'] / total_revenue * 100)
    print(f"   {idx:2}. {prod:30} ₹{row['total_amount']:12,.2f} ({rev_pct:5.2f}%) - {row['quantity']:,} units")

# Monthly trends
print(f"\n📅 MONTHLY REVENUE TREND:")
monthly = df.groupby(['month', 'month_name']).agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).reset_index()
monthly['avg_transaction'] = monthly['total_amount'] / monthly['transaction_id']

for _, row in monthly.iterrows():
    print(f"   {row['month_name']:12} ₹{row['total_amount']:12,.2f}  ({row['transaction_id']:6,} trans, Avg: ₹{row['avg_transaction']:.2f})")

# Best and worst performing months
best_month = monthly.loc[monthly['total_amount'].idxmax()]
worst_month = monthly.loc[monthly['total_amount'].idxmin()]
print(f"\n   💚 BEST MONTH:  {best_month['month_name']} - ₹{best_month['total_amount']:,.2f}")
print(f"   ❌ WORST MONTH: {worst_month['month_name']} - ₹{worst_month['total_amount']:,.2f}")
print(f"   📊 Variance: {((best_month['total_amount'] - worst_month['total_amount']) / worst_month['total_amount'] * 100):.1f}%")

# ============================================================================
# 2. CUSTOMER BEHAVIOR INSIGHTS
# ============================================================================
print("\n" + "=" * 100)
print("👥 2. CUSTOMER BEHAVIOR INSIGHTS")
print("=" * 100)

# Customer segmentation
print(f"\n🎯 CUSTOMER SEGMENTATION:")
cust_seg = df.groupby('customer_type').agg({
    'transaction_id': 'count',
    'total_amount': 'sum',
    'customer_id': 'nunique'
})
cust_seg['Avg_Trans_Value'] = cust_seg['total_amount'] / cust_seg['transaction_id']
cust_seg['Avg_Frequency'] = cust_seg['transaction_id'] / cust_seg['customer_id']
cust_seg['Revenue_%'] = (cust_seg['total_amount'] / total_revenue * 100).round(2)

for ctype, row in cust_seg.iterrows():
    print(f"\n   {ctype} Customers:")
    print(f"      - Count: {row['customer_id']:,} ({row['customer_id']/df['customer_id'].nunique()*100:.1f}% of base)")
    print(f"      - Revenue: ₹{row['total_amount']:,.2f} ({row['Revenue_%']:.1f}% of total)")
    print(f"      - Avg Transaction Value: ₹{row['Avg_Trans_Value']:.2f}")
    print(f"      - Avg Visits: {row['Avg_Frequency']:.2f}")

# Top customers
print(f"\n⭐ TOP 10 CUSTOMERS (VIP):")
top_customers = df.groupby('customer_id').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'customer_type': 'first'
}).sort_values('total_amount', ascending=False)

for idx, (cust_id, row) in enumerate(top_customers.head(10).iterrows(), 1):
    ltv_contribution = (row['total_amount'] / total_revenue * 100)
    print(f"   {idx:2}. {cust_id} ({row['customer_type']:10}) - ₹{row['total_amount']:10,.2f} ({row['transaction_id']:3} visits)")

# Age group analysis
print(f"\n👤 DEMOGRAPHICS - AGE GROUP ANALYSIS:")
age_analysis = df.groupby('age_group').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
})
age_analysis['Avg_Transaction'] = age_analysis['total_amount'] / age_analysis['transaction_id']
age_analysis = age_analysis.sort_values('total_amount', ascending=False)

for age, row in age_analysis.iterrows():
    rev_pct = (row['total_amount'] / total_revenue * 100)
    print(f"   {age:10} ₹{row['total_amount']:12,.2f} ({rev_pct:5.2f}%) - {row['customer_id']:,} customers, Avg: ₹{row['Avg_Transaction']:.2f}")

# ============================================================================
# 3. INVENTORY & STOCK MANAGEMENT
# ============================================================================
print("\n" + "=" * 100)
print("📦 3. INVENTORY & STOCK MANAGEMENT")
print("=" * 100)

# Fast moving items
print(f"\n🚀 FAST-MOVING ITEMS (Top 10 by Volume):")
fast_movers = df.groupby(['product_name', 'category']).agg({
    'quantity': 'sum',
    'transaction_id': 'count'
}).sort_values('quantity', ascending=False)

for idx, ((prod, cat), row) in enumerate(fast_movers.head(10).iterrows(), 1):
    avg_daily = row['quantity'] / 730  # 2 years = 730 days
    print(f"   {idx:2}. {prod:30} {row['quantity']:6,} units ({avg_daily:5.1f}/day) - {row['transaction_id']:,} trans")

# Slow moving items
print(f"\n🐌 SLOW-MOVING ITEMS (Bottom 10 by Volume):")
slow_movers = fast_movers.sort_values('quantity', ascending=True)

for idx, ((prod, cat), row) in enumerate(slow_movers.head(10).iterrows(), 1):
    avg_daily = row['quantity'] / 730
    print(f"   {idx:2}. {prod:30} {row['quantity']:6,} units ({avg_daily:5.2f}/day) - {row['transaction_id']:,} trans")

# Perishable items analysis
print(f"\n🥬 PERISHABLE ITEMS - WASTAGE RISK:")
perishable = df[df['days_to_expiry'].notna()].copy()
perishable_summary = perishable.groupby('category').agg({
    'days_to_expiry': 'mean',
    'discount_percentage': 'mean',
    'total_amount': 'sum',
    'quantity': 'sum'
})

for cat, row in perishable_summary.iterrows():
    wastage_risk = "🔴 HIGH" if row['days_to_expiry'] < 3 else ("🟡 MEDIUM" if row['days_to_expiry'] < 5 else "🟢 LOW")
    print(f"   {cat:20} Avg Expiry: {row['days_to_expiry']:.1f} days, Avg Discount: {row['discount_percentage']:.1f}% {wastage_risk}")

# Stock turnover by category
print(f"\n📊 STOCK TURNOVER RATE:")
turnover = df.groupby('category')['quantity'].sum().sort_values(ascending=False)
for cat, qty in turnover.items():
    daily_turnover = qty / 730
    print(f"   {cat:25} {qty:7,} units total ({daily_turnover:6.1f} units/day)")

# ============================================================================
# 4. PRICING & PROMOTIONS
# ============================================================================
print("\n" + "=" * 100)
print("💵 4. PRICING & PROMOTIONS EFFECTIVENESS")
print("=" * 100)

# Discount impact
print(f"\n🎁 DISCOUNT IMPACT ANALYSIS:")
discount_analysis = df.groupby(pd.cut(df['discount_percentage'], bins=[0, 5, 10, 20, 30, 100], right=False)).agg({
    'transaction_id': 'count',
    'total_amount': 'sum',
    'quantity': 'mean'
})
discount_analysis.index = ['No Discount (0-5%)', 'Low (5-10%)', 'Medium (10-20%)', 'High (20-30%)', 'Very High (30%+)']

for disc_range, row in discount_analysis.iterrows():
    trans_pct = (row['transaction_id'] / total_transactions * 100)
    rev_pct = (row['total_amount'] / total_revenue * 100)
    print(f"   {disc_range:22} {row['transaction_id']:7,} trans ({trans_pct:5.2f}%) - ₹{row['total_amount']:12,.2f} ({rev_pct:5.2f}%), Avg Qty: {row['quantity']:.2f}")

# Promotion effectiveness
print(f"\n📢 PROMOTION EFFECTIVENESS:")
promo_df = df[df['promotion_id'].notna()]
non_promo_df = df[df['promotion_id'].isna()]

print(f"   With Promotion:    {len(promo_df):,} trans ({len(promo_df)/len(df)*100:.2f}%) - ₹{promo_df['total_amount'].sum():,.2f} - Avg: ₹{promo_df['total_amount'].mean():.2f}")
print(f"   Without Promotion: {len(non_promo_df):,} trans ({len(non_promo_df)/len(df)*100:.2f}%) - ₹{non_promo_df['total_amount'].sum():,.2f} - Avg: ₹{non_promo_df['total_amount'].mean():.2f}")
print(f"\n   💡 Insight: Promotions increase avg transaction by ₹{(promo_df['total_amount'].mean() - non_promo_df['total_amount'].mean()):.2f}")

# Weekend vs weekday
print(f"\n📅 WEEKEND vs WEEKDAY PERFORMANCE:")
weekend_rev = df[df['is_weekend'] == True]['total_amount'].sum()
weekday_rev = df[df['is_weekend'] == False]['total_amount'].sum()
weekend_trans = len(df[df['is_weekend'] == True])
weekday_trans = len(df[df['is_weekend'] == False])

print(f"   Weekend:  ₹{weekend_rev:12,.2f} ({weekend_trans:,} trans) - Avg: ₹{weekend_rev/weekend_trans:.2f}")
print(f"   Weekday:  ₹{weekday_rev:12,.2f} ({weekday_trans:,} trans) - Avg: ₹{weekday_rev/weekday_trans:.2f}")
print(f"   💡 Weekend uplift: {((weekend_rev/weekend_trans) / (weekday_rev/weekday_trans) - 1) * 100:.1f}% per transaction")

# ============================================================================
# 5. OPERATIONAL EFFICIENCY
# ============================================================================
print("\n" + "=" * 100)
print("⚙️  5. OPERATIONAL EFFICIENCY")
print("=" * 100)

# Time slot analysis
print(f"\n🕐 HOURLY TRAFFIC PATTERN:")
hourly = df.groupby('time_slot').agg({
    'transaction_id': 'count',
    'total_amount': 'sum',
    'checkout_duration_sec': 'mean'
})
hourly['Pct_Traffic'] = (hourly['transaction_id'] / total_transactions * 100).round(2)
hourly['Avg_Trans'] = hourly['total_amount'] / hourly['transaction_id']

time_order = ['Early Morning (6-9 AM)', 'Morning (9-12 PM)', 'Afternoon (12-4 PM)', 'Evening (4-9 PM)', 'Night (9-11 PM)']
for slot in time_order:
    if slot in hourly.index:
        row = hourly.loc[slot]
        print(f"   {slot:25} {row['transaction_id']:7,} trans ({row['Pct_Traffic']:5.2f}%) - ₹{row['Avg_Trans']:7.2f} avg - {row['checkout_duration_sec']:.0f}s checkout")

# Peak hour identification
print(f"\n⏰ PEAK HOURS STAFFING RECOMMENDATION:")
peak_hours = df.groupby('hour').agg({
    'transaction_id': 'count',
    'total_amount': 'sum'
}).sort_values('transaction_id', ascending=False)

print(f"   Top 5 busiest hours:")
for hour, row in peak_hours.head().iterrows():
    traffic_pct = (row['transaction_id'] / total_transactions * 100)
    print(f"      {hour:2}:00 - {row['transaction_id']:,} trans ({traffic_pct:.2f}%) - Revenue: ₹{row['total_amount']:,.2f}")

# Store performance
print(f"\n🏪 STORE PERFORMANCE COMPARISON:")
store_perf = df.groupby(['store_id', 'store_type', 'store_region']).agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).reset_index()
store_perf['Avg_Trans'] = store_perf['total_amount'] / store_perf['transaction_id']
store_perf = store_perf.sort_values('total_amount', ascending=False)

print(f"\n   Top 10 Stores by Revenue:")
for idx, row in store_perf.head(10).iterrows():
    rev_pct = (row['total_amount'] / total_revenue * 100)
    print(f"   {row['store_id']} ({row['store_type']:11} | {row['store_region']:7}) - ₹{row['total_amount']:12,.2f} ({rev_pct:5.2f}%) - {row['transaction_id']:,} trans")

print(f"\n   Bottom 5 Stores (Need Attention):")
for idx, row in store_perf.tail(5).iterrows():
    rev_pct = (row['total_amount'] / total_revenue * 100)
    print(f"   {row['store_id']} ({row['store_type']:11} | {row['store_region']:7}) - ₹{row['total_amount']:12,.2f} ({rev_pct:5.2f}%) - {row['transaction_id']:,} trans")

# Payment method trends
print(f"\n💳 PAYMENT METHOD PREFERENCES:")
payment = df.groupby('payment_method').agg({
    'transaction_id': 'count',
    'total_amount': 'sum'
}).sort_values('transaction_id', ascending=False)

for method, row in payment.iterrows():
    trans_pct = (row['transaction_id'] / total_transactions * 100)
    print(f"   {method:15} {row['transaction_id']:7,} ({trans_pct:5.2f}%) - ₹{row['total_amount']:12,.2f}")

# ============================================================================
# 6. EXTERNAL FACTORS
# ============================================================================
print("\n" + "=" * 100)
print("🌤️  6. EXTERNAL FACTORS IMPACT")
print("=" * 100)

# Seasonal analysis
print(f"\n🌿 SEASONAL PERFORMANCE:")
seasonal = df.groupby('season').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'mean'
})
seasonal['Avg_Trans'] = seasonal['total_amount'] / seasonal['transaction_id']

for season, row in seasonal.iterrows():
    rev_pct = (row['total_amount'] / total_revenue * 100)
    print(f"   {season:10} ₹{row['total_amount']:12,.2f} ({rev_pct:5.2f}%) - {row['transaction_id']:,} trans - Avg: ₹{row['Avg_Trans']:.2f}")

# Weather impact
print(f"\n⛅ WEATHER IMPACT ON SALES:")
weather = df.groupby('weather_condition').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'mean'
})
weather['Avg_Trans'] = weather['total_amount'] / weather['transaction_id']

for condition, row in weather.iterrows():
    trans_pct = (row['transaction_id'] / total_transactions * 100)
    print(f"   {condition:10} {row['transaction_id']:7,} trans ({trans_pct:5.2f}%) - Avg: ₹{row['Avg_Trans']:7.2f} - Qty: {row['quantity']:.2f}")

# Holiday impact
print(f"\n🎉 HOLIDAY vs REGULAR DAY:")
holiday_rev = df[df['is_holiday'] == True]['total_amount'].sum()
regular_rev = df[df['is_holiday'] == False]['total_amount'].sum()
holiday_trans = len(df[df['is_holiday'] == True])
regular_trans = len(df[df['is_holiday'] == False])

print(f"   Holiday Days:  ₹{holiday_rev:12,.2f} ({holiday_trans:7,} trans) - Avg: ₹{holiday_rev/holiday_trans if holiday_trans > 0 else 0:.2f}")
print(f"   Regular Days:  ₹{regular_rev:12,.2f} ({regular_trans:7,} trans) - Avg: ₹{regular_rev/regular_trans:.2f}")
if holiday_trans > 0:
    print(f"   💡 Holiday uplift: {((holiday_rev/holiday_trans) / (regular_rev/regular_trans) - 1) * 100:.1f}% per transaction")

# ============================================================================
# 7. KEY RECOMMENDATIONS
# ============================================================================
print("\n" + "=" * 100)
print("💡 7. KEY RECOMMENDATIONS FOR STORE MANAGERS")
print("=" * 100)

print(f"""
🎯 IMMEDIATE ACTIONS:

1. INVENTORY OPTIMIZATION:
   → Increase stock for top 10 fast-moving products (especially during peak hours)
   → Review slow-moving items - consider clearance sales or discontinuation
   → Monitor perishable items with <3 days expiry - implement aggressive discounting
   → Adjust stock levels based on seasonal patterns (identified above)

2. STAFFING OPTIMIZATION:
   → Increase staff during Evening (4-9 PM) - handles {hourly.loc['Evening (4-9 PM)', 'Pct_Traffic'] if 'Evening (4-9 PM)' in hourly.index else 'N/A'}% of daily traffic
   → Reduce staff during low-traffic hours (Late Night, Early Morning)
   → Weekend staffing needs {((weekend_trans/104) / (weekday_trans/626) * 100):.0f}% increase vs weekday

3. PRICING & PROMOTIONS:
   → Premium customers ({cust_seg.loc['Premium', 'customer_id']:,}) contribute {cust_seg.loc['Premium', 'Revenue_%']:.1f}% revenue - offer exclusive deals
   → Target occasional customers with personalized promotions
   → Weather-based dynamic pricing (increase beverage prices on sunny days)
   → Holiday preparation: stock up 2-3 weeks before major festivals

4. CUSTOMER RETENTION:
   → Focus on retaining Regular customers (they contribute {cust_seg.loc['Regular', 'Revenue_%']:.1f}% of revenue)
   → Convert Occasional to Regular through loyalty programs
   → Age group {age_analysis.index[0]} is highest revenue - tailor marketing to this segment
   → Top 10 VIP customers need personalized attention

5. OPERATIONAL IMPROVEMENTS:
   → Promote UPI/Card payments to reduce cash handling (currently {payment.loc['UPI', 'transaction_id']/total_transactions*100:.1f}% UPI)
   → Optimize checkout process during peak hours (avg {hourly['checkout_duration_sec'].max():.0f}s checkout time)
   → Review bottom 5 stores for improvement opportunities
   → Ensure adequate stock of seasonal products before season starts

6. CATEGORY MANAGEMENT:
   → Top category ({cat_revenue.index[0]}) needs premium shelf space
   → Cross-sell complementary products (e.g., tea + biscuits, rice + dal)
   → Organic products command {((df[df['is_organic']==True]['unit_price'].mean() / df[df['is_organic']==False]['unit_price'].mean()) - 1) * 100:.0f}% premium - expand range
   → Monitor discount effectiveness - avoid over-discounting popular items
""")

print("=" * 100)
print("✅ ANALYSIS COMPLETE - Review insights and implement recommendations")
print("=" * 100)
