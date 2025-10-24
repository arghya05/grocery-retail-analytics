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

print("\nGenerating comprehensive KPI report...")

# Create a single consolidated KPI DataFrame
kpi_data = []

# ===== SECTION 1: OVERALL BUSINESS METRICS =====
kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Total Revenue',
    'Value': f"${df['total_amount'].sum():,.2f}",
    'Numeric_Value': df['total_amount'].sum()
})

kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Total Transactions',
    'Value': f"{len(df):,}",
    'Numeric_Value': len(df)
})

kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Total Items Sold',
    'Value': f"{df['quantity'].sum():,}",
    'Numeric_Value': df['quantity'].sum()
})

avg_txn_value = df.groupby('transaction_id')['total_amount'].sum().mean()
kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Average Transaction Value',
    'Value': f"${avg_txn_value:,.2f}",
    'Numeric_Value': avg_txn_value
})

kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Average Basket Size',
    'Value': f"{df['basket_size'].mean():.2f}",
    'Numeric_Value': df['basket_size'].mean()
})

avg_items_per_txn = df.groupby('transaction_id')['quantity'].sum().mean()
kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Average Items Per Transaction',
    'Value': f"{avg_items_per_txn:.2f}",
    'Numeric_Value': avg_items_per_txn
})

total_discount = df.apply(lambda x: x['unit_price'] * x['quantity'] * x['discount_percentage'] / 100, axis=1).sum()
kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Total Discount Given',
    'Value': f"${total_discount:,.2f}",
    'Numeric_Value': total_discount
})

kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Average Discount Percentage',
    'Value': f"{df['discount_percentage'].mean():.2f}%",
    'Numeric_Value': df['discount_percentage'].mean()
})

kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Total Unique Customers',
    'Value': f"{df['customer_id'].nunique():,}",
    'Numeric_Value': df['customer_id'].nunique()
})

kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Total Unique Products',
    'Value': f"{df['product_id'].nunique()}",
    'Numeric_Value': df['product_id'].nunique()
})

kpi_data.append({
    'Section': 'Overall Business',
    'KPI': 'Total Stores',
    'Value': f"{df['store_id'].nunique()}",
    'Numeric_Value': df['store_id'].nunique()
})

# ===== SECTION 2: TOP PERFORMERS =====
# Top Store
top_store = df.groupby('store_id')['total_amount'].sum().sort_values(ascending=False).iloc[0]
top_store_id = df.groupby('store_id')['total_amount'].sum().sort_values(ascending=False).index[0]
store_info = df[df['store_id'] == top_store_id][['store_region', 'store_type']].iloc[0]

kpi_data.append({
    'Section': 'Top Performers',
    'KPI': 'Top Store by Revenue',
    'Value': f"{top_store_id} - {store_info['store_region']} {store_info['store_type']} (${top_store:,.2f})",
    'Numeric_Value': top_store
})

# Top 3 Stores
top_3_stores = df.groupby('store_id')['total_amount'].sum().sort_values(ascending=False).head(3)
for idx, (store_id, revenue) in enumerate(top_3_stores.items(), 2):
    kpi_data.append({
        'Section': 'Top Performers',
        'KPI': f'Top Store #{idx} by Revenue',
        'Value': f"{store_id} (${revenue:,.2f})",
        'Numeric_Value': revenue
    })

# Top Category
top_category = df.groupby('category')['total_amount'].sum().sort_values(ascending=False).iloc[0]
top_category_name = df.groupby('category')['total_amount'].sum().sort_values(ascending=False).index[0]

kpi_data.append({
    'Section': 'Top Performers',
    'KPI': 'Top Category by Revenue',
    'Value': f"{top_category_name} (${top_category:,.2f})",
    'Numeric_Value': top_category
})

# Top 3 Products
top_3_products = df.groupby(['product_name', 'category'])['total_amount'].sum().sort_values(ascending=False).head(3)
for idx, ((product, category), revenue) in enumerate(top_3_products.items(), 1):
    kpi_data.append({
        'Section': 'Top Performers',
        'KPI': f'Top Product #{idx}',
        'Value': f"{product} - {category} (${revenue:,.2f})",
        'Numeric_Value': revenue
    })

# Top Brand
top_brand = df.groupby('brand')['total_amount'].sum().sort_values(ascending=False).iloc[0]
top_brand_name = df.groupby('brand')['total_amount'].sum().sort_values(ascending=False).index[0]

kpi_data.append({
    'Section': 'Top Performers',
    'KPI': 'Top Brand by Revenue',
    'Value': f"{top_brand_name} (${top_brand:,.2f})",
    'Numeric_Value': top_brand
})

# ===== SECTION 3: STORE PERFORMANCE =====
store_performance = df.groupby('store_id').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).mean()

kpi_data.append({
    'Section': 'Store Performance',
    'KPI': 'Average Revenue Per Store',
    'Value': f"${store_performance['total_amount']:,.2f}",
    'Numeric_Value': store_performance['total_amount']
})

kpi_data.append({
    'Section': 'Store Performance',
    'KPI': 'Average Transactions Per Store',
    'Value': f"{store_performance['transaction_id']:,.0f}",
    'Numeric_Value': store_performance['transaction_id']
})

kpi_data.append({
    'Section': 'Store Performance',
    'KPI': 'Average Customers Per Store',
    'Value': f"{store_performance['customer_id']:,.0f}",
    'Numeric_Value': store_performance['customer_id']
})

# Performance by Store Type
store_type_perf = df.groupby('store_type')['total_amount'].sum().sort_values(ascending=False)
for store_type, revenue in store_type_perf.items():
    kpi_data.append({
        'Section': 'Store Performance',
        'KPI': f'{store_type} Stores Revenue',
        'Value': f"${revenue:,.2f}",
        'Numeric_Value': revenue
    })

# Performance by Region
region_perf = df.groupby('store_region')['total_amount'].sum().sort_values(ascending=False)
for region, revenue in region_perf.items():
    kpi_data.append({
        'Section': 'Store Performance',
        'KPI': f'{region} Region Revenue',
        'Value': f"${revenue:,.2f}",
        'Numeric_Value': revenue
    })

# ===== SECTION 4: CATEGORY PERFORMANCE =====
category_perf = df.groupby('category').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum'
}).sort_values('total_amount', ascending=False)

for idx, (category, row) in enumerate(category_perf.iterrows(), 1):
    kpi_data.append({
        'Section': 'Category Performance',
        'KPI': f'{category} - Revenue',
        'Value': f"${row['total_amount']:,.2f}",
        'Numeric_Value': row['total_amount']
    })
    kpi_data.append({
        'Section': 'Category Performance',
        'KPI': f'{category} - Transactions',
        'Value': f"{row['transaction_id']:,}",
        'Numeric_Value': row['transaction_id']
    })
    kpi_data.append({
        'Section': 'Category Performance',
        'KPI': f'{category} - Items Sold',
        'Value': f"{row['quantity']:,}",
        'Numeric_Value': row['quantity']
    })

# ===== SECTION 5: CUSTOMER INSIGHTS =====
customer_segment = df.groupby('customer_type').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count',
    'customer_id': 'nunique'
})

for customer_type in customer_segment.index:
    kpi_data.append({
        'Section': 'Customer Insights',
        'KPI': f'{customer_type} Customers - Total Revenue',
        'Value': f"${customer_segment.loc[customer_type, ('total_amount', 'sum')]:,.2f}",
        'Numeric_Value': customer_segment.loc[customer_type, ('total_amount', 'sum')]
    })
    kpi_data.append({
        'Section': 'Customer Insights',
        'KPI': f'{customer_type} Customers - Avg Transaction Value',
        'Value': f"${customer_segment.loc[customer_type, ('total_amount', 'mean')]:,.2f}",
        'Numeric_Value': customer_segment.loc[customer_type, ('total_amount', 'mean')]
    })
    kpi_data.append({
        'Section': 'Customer Insights',
        'KPI': f'{customer_type} Customers - Count',
        'Value': f"{customer_segment.loc[customer_type, ('customer_id', 'nunique')]:,}",
        'Numeric_Value': customer_segment.loc[customer_type, ('customer_id', 'nunique')]
    })

# Age Group Analysis
age_perf = df.groupby('age_group')['total_amount'].sum().sort_values(ascending=False)
for age_group, revenue in age_perf.items():
    kpi_data.append({
        'Section': 'Customer Insights',
        'KPI': f'Age Group {age_group} - Revenue',
        'Value': f"${revenue:,.2f}",
        'Numeric_Value': revenue
    })

# Gender Analysis
gender_perf = df.groupby('gender')['total_amount'].sum().sort_values(ascending=False)
for gender, revenue in gender_perf.items():
    kpi_data.append({
        'Section': 'Customer Insights',
        'KPI': f'{gender} Customers - Revenue',
        'Value': f"${revenue:,.2f}",
        'Numeric_Value': revenue
    })

# ===== SECTION 6: OPERATIONAL METRICS =====
# Payment Methods
payment_perf = df.groupby('payment_method').agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).sort_values('transaction_id', ascending=False)

for payment, row in payment_perf.iterrows():
    kpi_data.append({
        'Section': 'Operational Metrics',
        'KPI': f'{payment} - Transactions',
        'Value': f"{row['transaction_id']:,} ({row['transaction_id']/len(df)*100:.1f}%)",
        'Numeric_Value': row['transaction_id']
    })
    kpi_data.append({
        'Section': 'Operational Metrics',
        'KPI': f'{payment} - Revenue',
        'Value': f"${row['total_amount']:,.2f}",
        'Numeric_Value': row['total_amount']
    })

# Time Slot Performance
timeslot_perf = df.groupby('time_slot').agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).sort_values('transaction_id', ascending=False)

for timeslot, row in timeslot_perf.iterrows():
    kpi_data.append({
        'Section': 'Operational Metrics',
        'KPI': f'{timeslot} - Transactions',
        'Value': f"{row['transaction_id']:,} ({row['transaction_id']/len(df)*100:.1f}%)",
        'Numeric_Value': row['transaction_id']
    })

# Delivery Method
delivery_perf = df.groupby('delivery_method').agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).sort_values('transaction_id', ascending=False)

for delivery, row in delivery_perf.iterrows():
    kpi_data.append({
        'Section': 'Operational Metrics',
        'KPI': f'{delivery} - Transactions',
        'Value': f"{row['transaction_id']:,} ({row['transaction_id']/len(df)*100:.1f}%)",
        'Numeric_Value': row['transaction_id']
    })
    kpi_data.append({
        'Section': 'Operational Metrics',
        'KPI': f'{delivery} - Revenue',
        'Value': f"${row['total_amount']:,.2f}",
        'Numeric_Value': row['total_amount']
    })

# Average Checkout Duration
avg_checkout = df['checkout_duration_sec'].mean()
kpi_data.append({
    'Section': 'Operational Metrics',
    'KPI': 'Average Checkout Duration',
    'Value': f"{avg_checkout:.0f} seconds ({avg_checkout/60:.1f} minutes)",
    'Numeric_Value': avg_checkout
})

# ===== SECTION 7: PRODUCT INSIGHTS =====
# Organic vs Non-Organic
organic_perf = df.groupby('is_organic').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'quantity': 'sum'
})

for is_organic, row in organic_perf.iterrows():
    product_type = 'Organic' if is_organic else 'Non-Organic'
    kpi_data.append({
        'Section': 'Product Insights',
        'KPI': f'{product_type} Products - Revenue',
        'Value': f"${row['total_amount']:,.2f}",
        'Numeric_Value': row['total_amount']
    })
    kpi_data.append({
        'Section': 'Product Insights',
        'KPI': f'{product_type} Products - Transactions',
        'Value': f"{row['transaction_id']:,} ({row['transaction_id']/len(df)*100:.1f}%)",
        'Numeric_Value': row['transaction_id']
    })

# Brand Performance - Top 10
brand_perf = df.groupby('brand')['total_amount'].sum().sort_values(ascending=False).head(10)
for idx, (brand, revenue) in enumerate(brand_perf.items(), 1):
    kpi_data.append({
        'Section': 'Product Insights',
        'KPI': f'Top Brand #{idx}',
        'Value': f"{brand} (${revenue:,.2f})",
        'Numeric_Value': revenue
    })

# ===== SECTION 8: TIME-BASED TRENDS =====
# Weekend vs Weekday
weekend_perf = df.groupby('is_weekend').agg({
    'total_amount': ['sum', 'mean'],
    'transaction_id': 'count'
})

for is_weekend, row in weekend_perf.iterrows():
    day_type = 'Weekend' if is_weekend else 'Weekday'
    kpi_data.append({
        'Section': 'Time-Based Trends',
        'KPI': f'{day_type} - Total Revenue',
        'Value': f"${row[('total_amount', 'sum')]:,.2f}",
        'Numeric_Value': row[('total_amount', 'sum')]
    })
    kpi_data.append({
        'Section': 'Time-Based Trends',
        'KPI': f'{day_type} - Avg Transaction Value',
        'Value': f"${row[('total_amount', 'mean')]:,.2f}",
        'Numeric_Value': row[('total_amount', 'mean')]
    })
    kpi_data.append({
        'Section': 'Time-Based Trends',
        'KPI': f'{day_type} - Transactions',
        'Value': f"{row[('transaction_id', 'count')]:,} ({row[('transaction_id', 'count')]/len(df)*100:.1f}%)",
        'Numeric_Value': row[('transaction_id', 'count')]
    })

# Seasonal Performance
season_perf = df.groupby('season')['total_amount'].sum().sort_values(ascending=False)
for season, revenue in season_perf.items():
    kpi_data.append({
        'Section': 'Time-Based Trends',
        'KPI': f'{season} Season - Revenue',
        'Value': f"${revenue:,.2f}",
        'Numeric_Value': revenue
    })

# Monthly Performance - Last 6 months
monthly_perf = df.groupby('month').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).sort_index(ascending=False).head(6)

for month, row in monthly_perf.iterrows():
    kpi_data.append({
        'Section': 'Time-Based Trends',
        'KPI': f'{month} - Revenue',
        'Value': f"${row['total_amount']:,.2f}",
        'Numeric_Value': row['total_amount']
    })
    kpi_data.append({
        'Section': 'Time-Based Trends',
        'KPI': f'{month} - Transactions',
        'Value': f"{row['transaction_id']:,}",
        'Numeric_Value': row['transaction_id']
    })

# ===== SECTION 9: LOYALTY & PROMOTIONS =====
total_loyalty_earned = df['loyalty_points_earned'].sum()
total_loyalty_used = df['loyalty_points_used'].sum()

kpi_data.append({
    'Section': 'Loyalty & Promotions',
    'KPI': 'Total Loyalty Points Earned',
    'Value': f"{total_loyalty_earned:,}",
    'Numeric_Value': total_loyalty_earned
})

kpi_data.append({
    'Section': 'Loyalty & Promotions',
    'KPI': 'Total Loyalty Points Used',
    'Value': f"{total_loyalty_used:,}",
    'Numeric_Value': total_loyalty_used
})

kpi_data.append({
    'Section': 'Loyalty & Promotions',
    'KPI': 'Net Loyalty Points',
    'Value': f"{total_loyalty_earned - total_loyalty_used:,}",
    'Numeric_Value': total_loyalty_earned - total_loyalty_used
})

# Transactions with Promotions
promo_txns = df['promotion_id'].notna().sum()
kpi_data.append({
    'Section': 'Loyalty & Promotions',
    'KPI': 'Transactions with Promotions',
    'Value': f"{promo_txns:,} ({promo_txns/len(df)*100:.1f}%)",
    'Numeric_Value': promo_txns
})

# ===== CREATE FINAL DATAFRAME AND SAVE =====
kpi_df = pd.DataFrame(kpi_data)

# Reorder columns for better readability
kpi_df = kpi_df[['Section', 'KPI', 'Value', 'Numeric_Value']]

# Save to CSV
kpi_df.to_csv('store_manager_kpi_dashboard.csv', index=False)

print("\n" + "="*70)
print("COMPREHENSIVE KPI DASHBOARD CREATED SUCCESSFULLY!")
print("="*70)
print(f"\nFile: store_manager_kpi_dashboard.csv")
print(f"Total KPIs: {len(kpi_df)}")
print(f"\nKPI Sections:")
for section in kpi_df['Section'].unique():
    count = len(kpi_df[kpi_df['Section'] == section])
    print(f"  - {section}: {count} KPIs")
print("="*70)

# Also create a summary view
print("\n\nKEY HIGHLIGHTS:")
print("-" * 70)
for _, row in kpi_df[kpi_df['Section'] == 'Overall Business'].iterrows():
    print(f"{row['KPI']}: {row['Value']}")
print("\nTOP PERFORMERS:")
for _, row in kpi_df[kpi_df['Section'] == 'Top Performers'].head(5).iterrows():
    print(f"{row['KPI']}: {row['Value']}")
print("="*70)
