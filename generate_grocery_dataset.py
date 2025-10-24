import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import warnings
warnings.filterwarnings('ignore')

fake = Faker('en_IN')
np.random.seed(42)
random.seed(42)
Faker.seed(42)

print("Starting Grocery Dataset Generation...")
print("=" * 60)
print("Target: 2,000,000 transactions in a single CSV file")
print("This may take several minutes...")
print("=" * 60)

# ============================================================================
# REFERENCE DATA SETUP
# ============================================================================

# Store reference data
store_regions = ['North', 'South', 'East', 'West', 'Central']
store_types = ['Supermarket', 'Hypermarket', 'Express']
cities_by_tier = {
    'Metro': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune'],
    'Tier-2': ['Jaipur', 'Lucknow', 'Nagpur', 'Indore', 'Coimbatore', 'Kochi', 'Visakhapatnam', 'Bhopal'],
    'Tier-3': ['Mysore', 'Udaipur', 'Nashik', 'Vadodara', 'Rajkot', 'Madurai']
}

# Create store lookup (50 stores)
stores_lookup = []
store_id = 1
for tier, count in [('Metro', 15), ('Tier-2', 20), ('Tier-3', 15)]:
    cities = cities_by_tier[tier]
    for i in range(count):
        stores_lookup.append({
            'store_id': f'STR_{store_id:03d}',
            'region': random.choice(store_regions),
            'store_type': random.choice(store_types),
            'tier': tier
        })
        store_id += 1

# Product categories and details
categories = {
    'Staples & Grains': {
        'products': ['Basmati Rice', 'Regular Rice', 'Wheat Flour', 'Moong Dal', 'Toor Dal', 'Chickpeas', 'Rajma'],
        'price_range': (50, 500),
        'brands': ['Fortune', 'India Gate', 'Tata Sampann', 'Aashirvaad', 'Local'],
        'weight': 0.20
    },
    'Dairy Products': {
        'products': ['Milk', 'Curd', 'Paneer', 'Butter', 'Cheese', 'Ghee', 'Lassi'],
        'price_range': (30, 400),
        'brands': ['Amul', 'Mother Dairy', 'Britannia', 'Nestle', 'Local'],
        'weight': 0.15
    },
    'Fresh Produce': {
        'products': ['Tomato', 'Onion', 'Potato', 'Carrot', 'Apple', 'Banana', 'Orange', 'Spinach', 'Cabbage'],
        'price_range': (20, 200),
        'brands': ['Local', 'Organic Farms', 'Fresh Direct'],
        'weight': 0.12
    },
    'Beverages': {
        'products': ['Tea', 'Coffee', 'Orange Juice', 'Mango Juice', 'Soft Drink', 'Energy Drink', 'Coconut Water'],
        'price_range': (20, 300),
        'brands': ['Tata Tea', 'Nescafe', 'Bru', 'Real', 'Coca-Cola', 'Pepsi', 'Red Bull'],
        'weight': 0.10
    },
    'Snacks & Confectionery': {
        'products': ['Potato Chips', 'Biscuits', 'Chocolate', 'Namkeen', 'Cookies', 'Wafers'],
        'price_range': (10, 250),
        'brands': ['Lays', 'Parle', 'Cadbury', 'Haldiram', 'Britannia', 'ITC'],
        'weight': 0.10
    },
    'Cooking Essentials': {
        'products': ['Cooking Oil', 'Salt', 'Sugar', 'Turmeric', 'Chili Powder', 'Garam Masala', 'Coriander Powder'],
        'price_range': (20, 500),
        'brands': ['Fortune', 'Tata', 'Everest', 'MDH', 'Catch'],
        'weight': 0.08
    },
    'Personal Care': {
        'products': ['Soap', 'Shampoo', 'Toothpaste', 'Body Wash', 'Face Cream', 'Hair Oil'],
        'price_range': (30, 500),
        'brands': ['Dettol', 'Dove', 'Pantene', 'Colgate', 'Ponds', 'Parachute'],
        'weight': 0.08
    },
    'Household Items': {
        'products': ['Detergent', 'Dish Wash', 'Floor Cleaner', 'Toilet Cleaner', 'Air Freshener'],
        'price_range': (50, 400),
        'brands': ['Surf Excel', 'Vim', 'Harpic', 'Lizol', 'Ambipur'],
        'weight': 0.07
    },
    'Bakery': {
        'products': ['Bread', 'Buns', 'Cake', 'Cookies', 'Pastries'],
        'price_range': (20, 300),
        'brands': ['Britannia', 'Modern', 'Harvest Gold', 'Local Bakery'],
        'weight': 0.05
    },
    'Frozen Foods': {
        'products': ['Ice Cream', 'Frozen Peas', 'Frozen Corn', 'French Fries', 'Frozen Paneer'],
        'price_range': (50, 400),
        'brands': ['Amul', 'Kwality Walls', 'Vadilal', 'McCain'],
        'weight': 0.05
    }
}

# Create product lookup (500 products)
products_lookup = []
product_id = 1
sub_categories = ['Regular', 'Premium', 'Economy', 'Organic']
variants = ['500g', '1kg', '5kg', '1L', '500ml', '250ml', '100g', '200g', 'Pack of 2', 'Pack of 4']

for category, details in categories.items():
    num_products = int(500 * details['weight'])
    for i in range(num_products):
        base_product = random.choice(details['products'])
        variant = random.choice(variants)
        is_perishable = category in ['Dairy Products', 'Fresh Produce', 'Bakery', 'Frozen Foods']
        has_organic = 'Organic' in details['brands'] or category == 'Fresh Produce'

        products_lookup.append({
            'product_id': f'PRD_{product_id:05d}',
            'product_name': f'{base_product} {variant}',
            'category': category,
            'sub_category': random.choice(sub_categories),
            'brand': random.choice(details['brands']),
            'unit_price': round(random.uniform(*details['price_range']), 2),
            'is_organic': random.choice([True, False]) if has_organic else False,
            'origin_country': random.choice(['India', 'USA', 'Thailand', 'Sri Lanka', 'Australia']) if category in ['Fresh Produce', 'Staples & Grains'] else 'India',
            'is_perishable': is_perishable
        })
        product_id += 1

# Date range and temporal data
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

indian_holidays = [
    '2022-01-26', '2022-03-18', '2022-04-14', '2022-05-03', '2022-08-15', '2022-08-31', '2022-10-05', '2022-10-24', '2022-11-08', '2022-12-25',
    '2023-01-26', '2023-03-08', '2023-04-14', '2023-05-05', '2023-08-15', '2023-09-19', '2023-10-02', '2023-10-24', '2023-11-12', '2023-12-25'
]
holiday_dates = set([datetime.strptime(d, '%Y-%m-%d').date() for d in indian_holidays])

time_slots = {
    'Early Morning': (6, 9),
    'Morning': (9, 12),
    'Afternoon': (12, 16),
    'Evening': (16, 21),
    'Night': (21, 23)
}

weather_conditions = ['Sunny', 'Rainy', 'Cloudy', 'Stormy']
payment_methods = ['Cash', 'Card', 'UPI', 'Wallet', 'Credit']
delivery_methods = ['In-store', 'Home Delivery', 'Click & Collect']
customer_types = ['Regular', 'Premium', 'New', 'Occasional']
age_groups = ['18-25', '26-35', '36-45', '46-60', '60+']
genders = ['Male', 'Female', 'Other']
seasons = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Summer',
           6: 'Summer', 7: 'Monsoon', 8: 'Monsoon', 9: 'Monsoon',
           10: 'Winter', 11: 'Winter', 12: 'Winter'}

# ============================================================================
# TRANSACTION DATA GENERATION (2,000,000 rows)
# ============================================================================

transactions_data = []
transaction_id = 1

BATCH_SIZE = 100000
NUM_BATCHES = 20

for batch_num in range(NUM_BATCHES):
    print(f"\nBatch {batch_num + 1}/{NUM_BATCHES}...")
    batch_transactions = []

    for i in range(BATCH_SIZE):
        # Date and time
        trans_date = random.choice(date_range)
        is_weekend = trans_date.weekday() >= 5
        is_holiday = trans_date.date() in holiday_dates

        # Time slot
        time_slot = random.choices(
            list(time_slots.keys()),
            weights=[0.15, 0.20, 0.15, 0.35, 0.15]
        )[0]

        hour_range = time_slots[time_slot]
        trans_hour = random.randint(hour_range[0], hour_range[1] - 1)
        trans_minute = random.randint(0, 59)
        trans_second = random.randint(0, 59)
        timestamp = trans_date.replace(hour=trans_hour, minute=trans_minute, second=trans_second)

        # Store
        store = random.choice(stores_lookup)

        # Product
        product = random.choice(products_lookup)

        # Customer details
        customer_id = f'CUST_{random.randint(1, 200000):06d}'
        customer_type = random.choices(customer_types, weights=[0.30, 0.10, 0.20, 0.40])[0]
        age_group = random.choices(age_groups, weights=[0.10, 0.35, 0.30, 0.20, 0.05])[0]
        gender = random.choices(genders, weights=[0.48, 0.50, 0.02])[0]

        # Basket size based on customer type
        if customer_type == 'Premium':
            basket_size = random.randint(10, 50)
        elif customer_type == 'Regular':
            basket_size = random.randint(5, 30)
        else:
            basket_size = random.randint(1, 15)

        # Quantity
        quantity = random.randint(1, min(10, basket_size))

        # Pricing
        unit_price = product['unit_price']

        # Discount logic
        if is_holiday or is_weekend:
            discount_percentage = random.choice([0, 5, 10, 15, 20, 25])
        else:
            discount_percentage = random.choice([0, 0, 0, 5, 10])

        final_price = unit_price * (1 - discount_percentage / 100)
        total_amount = round(quantity * final_price, 2)

        # Loyalty points
        loyalty_balance = random.randint(0, 5000) if random.random() > 0.3 else 0
        loyalty_points_used = random.randint(0, min(100, loyalty_balance)) if loyalty_balance > 0 and random.random() > 0.7 else 0
        loyalty_points_earned = int(total_amount * 0.01)

        # Promotion
        promotion_id = f'PROMO_{random.randint(1, 50):03d}' if random.random() > 0.7 else None

        # Weather and season
        season = seasons[trans_date.month]
        if season == 'Monsoon':
            weather = random.choices(weather_conditions, weights=[0.2, 0.5, 0.2, 0.1])[0]
        elif season == 'Summer':
            weather = random.choices(weather_conditions, weights=[0.7, 0.1, 0.15, 0.05])[0]
        else:
            weather = random.choices(weather_conditions, weights=[0.5, 0.2, 0.25, 0.05])[0]

        temperature = random.randint(15, 25) if season == 'Winter' else (random.randint(25, 35) if season == 'Summer' else random.randint(20, 32))

        # Other fields
        stock_level = random.randint(50, 1000)
        days_to_expiry = random.randint(1, 30) if product['is_perishable'] else None
        checkout_duration = random.randint(30, 300)
        shelf_location = f'Aisle {random.randint(1, 20)}' if random.random() > 0.2 else random.choice(['End Cap', 'Promo Display'])

        batch_transactions.append({
            'transaction_id': f'TXN_2022{transaction_id:012d}',
            'timestamp': timestamp,
            'store_id': store['store_id'],
            'store_region': store['region'],
            'store_type': store['store_type'],
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'category': product['category'],
            'sub_category': product['sub_category'],
            'brand': product['brand'],
            'quantity': quantity,
            'unit_price': unit_price,
            'discount_percentage': discount_percentage,
            'final_price': round(final_price, 2),
            'total_amount': total_amount,
            'payment_method': random.choices(payment_methods, weights=[0.15, 0.25, 0.40, 0.10, 0.10])[0],
            'customer_id': customer_id,
            'customer_type': customer_type,
            'loyalty_points_used': loyalty_points_used,
            'loyalty_points_earned': loyalty_points_earned,
            'age_group': age_group,
            'gender': gender,
            'basket_size': basket_size,
            'is_weekend': is_weekend,
            'is_holiday': is_holiday,
            'season': season,
            'promotion_id': promotion_id,
            'stock_level_at_sale': stock_level,
            'supplier_id': f'SUP_{random.randint(1, 100):03d}',
            'days_to_expiry': days_to_expiry,
            'weather_condition': weather,
            'temperature_celsius': temperature,
            'delivery_method': random.choices(delivery_methods, weights=[0.70, 0.20, 0.10])[0],
            'time_slot': time_slot,
            'employee_id': f'EMP_{random.randint(1, 500):03d}',
            'checkout_duration_sec': checkout_duration,
            'origin_country': product['origin_country'],
            'is_organic': product['is_organic'],
            'shelf_location': shelf_location
        })

        transaction_id += 1

        if (i + 1) % 10000 == 0:
            print(f"  Generated {i + 1:,} transactions...", end='\r')

    transactions_data.extend(batch_transactions)
    print(f"  ✓ Completed {len(transactions_data):,} total transactions")

print("\n" + "=" * 60)
print("Creating DataFrame and exporting to CSV...")

transactions_df = pd.DataFrame(transactions_data)

print("\nDataset Statistics:")
print("=" * 60)
print(f"Total Transactions: {len(transactions_df):,}")
print(f"Date Range: {transactions_df['timestamp'].min()} to {transactions_df['timestamp'].max()}")
print(f"Total Revenue: ₹{transactions_df['total_amount'].sum():,.2f}")
print(f"Average Transaction: ₹{transactions_df['total_amount'].mean():.2f}")
print(f"Unique Customers: {transactions_df['customer_id'].nunique():,}")
print(f"Unique Products: {transactions_df['product_id'].nunique():,}")
print(f"Unique Stores: {transactions_df['store_id'].nunique():,}")
print("=" * 60)

print("\nExporting to CSV file...")
transactions_df.to_csv('grocery_dataset.csv', index=False)

print("\n" + "=" * 60)
print("✓ DATASET GENERATION COMPLETE!")
print("=" * 60)
print("\nGenerated File: grocery_dataset.csv")
print(f"Total Rows: {len(transactions_df):,}")
print(f"Total Columns: {len(transactions_df.columns)}")
print("Estimated File Size: ~600-700 MB")
print("=" * 60)
