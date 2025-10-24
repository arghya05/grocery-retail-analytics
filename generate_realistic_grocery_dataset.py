import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
random.seed(42)

print("=" * 80)
print("REALISTIC GROCERY STORE DATASET GENERATOR")
print("=" * 80)
print("Generating 2,000,000 transactions with realistic business patterns...")
print()

# ============================================================================
# REALISTIC REFERENCE DATA WITH BUSINESS LOGIC
# ============================================================================

# Store tiers affect pricing and product mix
store_tiers = {
    'Metro': {'price_multiplier': 1.15, 'premium_prob': 0.4, 'stores': 15},
    'Tier-2': {'price_multiplier': 1.05, 'premium_prob': 0.2, 'stores': 20},
    'Tier-3': {'price_multiplier': 1.0, 'premium_prob': 0.1, 'stores': 15}
}

stores_lookup = []
store_id = 1
for tier, config in store_tiers.items():
    for i in range(config['stores']):
        stores_lookup.append({
            'store_id': f'STR_{store_id:03d}',
            'tier': tier,
            'region': random.choice(['North', 'South', 'East', 'West', 'Central']),
            'store_type': random.choice(['Hypermarket', 'Supermarket', 'Express']),
            'price_multiplier': config['price_multiplier'],
            'premium_prob': config['premium_prob']
        })
        store_id += 1

# Product categories with realistic seasonal and weather correlations
categories = {
    'Staples & Grains': {
        'products': [
            ('Basmati Rice 5kg', 350, 0.15), ('Rice 10kg', 500, 0.12), ('Wheat Flour 5kg', 220, 0.10),
            ('Moong Dal 1kg', 120, 0.08), ('Toor Dal 1kg', 140, 0.08), ('Chickpeas 500g', 65, 0.06),
            ('Rajma 500g', 85, 0.05)
        ],
        'brands': ['Fortune', 'India Gate', 'Tata Sampann', 'Aashirvaad'],
        'seasonal_boost': {'Monsoon': 1.2, 'Winter': 1.1},
        'weather_impact': {'Rainy': 1.15},
        'is_perishable': False
    },
    'Dairy Products': {
        'products': [
            ('Milk 1L', 60, 0.25), ('Curd 400g', 35, 0.15), ('Paneer 200g', 90, 0.10),
            ('Butter 100g', 55, 0.08), ('Cheese 200g', 150, 0.06), ('Ghee 500ml', 280, 0.05)
        ],
        'brands': ['Amul', 'Mother Dairy', 'Britannia', 'Nestle'],
        'seasonal_boost': {'Summer': 0.85, 'Winter': 1.1},
        'weather_impact': {'Sunny': 0.9},
        'is_perishable': True,
        'avg_expiry_days': 7
    },
    'Fresh Produce': {
        'products': [
            ('Tomato 1kg', 40, 0.12), ('Onion 1kg', 35, 0.12), ('Potato 1kg', 30, 0.11),
            ('Carrot 500g', 25, 0.08), ('Apple 1kg', 150, 0.09), ('Banana 1 dozen', 60, 0.10),
            ('Orange 1kg', 80, 0.07), ('Spinach 500g', 20, 0.06)
        ],
        'brands': ['Local Farm', 'Organic Valley', 'Fresh Direct'],
        'seasonal_boost': {'Monsoon': 1.3, 'Winter': 1.2},
        'weather_impact': {'Rainy': 1.25, 'Stormy': 1.4},
        'is_perishable': True,
        'avg_expiry_days': 5
    },
    'Beverages': {
        'products': [
            ('Tea 250g', 120, 0.15), ('Coffee 200g', 280, 0.10), ('Soft Drink 2L', 90, 0.12),
            ('Mango Juice 1L', 85, 0.08), ('Orange Juice 1L', 95, 0.07), ('Energy Drink 250ml', 120, 0.05)
        ],
        'brands': ['Tata Tea', 'Nescafe', 'Coca-Cola', 'Pepsi', 'Real', 'Red Bull'],
        'seasonal_boost': {'Summer': 1.4, 'Monsoon': 0.9},
        'weather_impact': {'Sunny': 1.3, 'Rainy': 0.8},
        'is_perishable': False
    },
    'Snacks & Confectionery': {
        'products': [
            ('Potato Chips 100g', 20, 0.15), ('Biscuits 200g', 25, 0.15), ('Chocolate 50g', 30, 0.12),
            ('Namkeen 200g', 35, 0.10), ('Cookies 150g', 40, 0.08), ('Wafers 100g', 25, 0.07)
        ],
        'brands': ['Lays', 'Parle', 'Cadbury', 'Haldiram', 'Britannia'],
        'seasonal_boost': {'Winter': 1.2},
        'weather_impact': {'Rainy': 1.15},
        'is_perishable': False
    },
    'Cooking Essentials': {
        'products': [
            ('Cooking Oil 1L', 180, 0.20), ('Salt 1kg', 20, 0.12), ('Sugar 1kg', 45, 0.12),
            ('Turmeric 100g', 35, 0.08), ('Chili Powder 100g', 40, 0.08), ('Garam Masala 50g', 45, 0.06)
        ],
        'brands': ['Fortune', 'Tata', 'Everest', 'MDH', 'Catch'],
        'seasonal_boost': {},
        'weather_impact': {},
        'is_perishable': False
    },
    'Personal Care': {
        'products': [
            ('Soap 125g', 35, 0.18), ('Shampoo 200ml', 150, 0.15), ('Toothpaste 150g', 80, 0.15),
            ('Body Wash 250ml', 185, 0.10), ('Face Cream 50g', 220, 0.08)
        ],
        'brands': ['Dettol', 'Dove', 'Pantene', 'Colgate', 'Ponds'],
        'seasonal_boost': {'Summer': 1.15},
        'weather_impact': {},
        'is_perishable': False
    },
    'Household Items': {
        'products': [
            ('Detergent 1kg', 180, 0.25), ('Dish Wash 500ml', 90, 0.20), ('Floor Cleaner 500ml', 85, 0.15),
            ('Toilet Cleaner 500ml', 95, 0.12), ('Air Freshener 250ml', 110, 0.08)
        ],
        'brands': ['Surf Excel', 'Vim', 'Harpic', 'Lizol', 'Ambipur'],
        'seasonal_boost': {},
        'weather_impact': {},
        'is_perishable': False
    },
    'Bakery': {
        'products': [
            ('Bread 400g', 35, 0.30), ('Buns Pack of 6', 30, 0.20), ('Cake 500g', 150, 0.12),
            ('Cookies 200g', 45, 0.10), ('Pastries Pack of 4', 80, 0.08)
        ],
        'brands': ['Britannia', 'Modern', 'Harvest Gold'],
        'seasonal_boost': {},
        'weather_impact': {},
        'is_perishable': True,
        'avg_expiry_days': 3
    },
    'Frozen Foods': {
        'products': [
            ('Ice Cream 500ml', 150, 0.30), ('Frozen Peas 500g', 65, 0.20), ('French Fries 400g', 120, 0.15),
            ('Frozen Corn 400g', 70, 0.10), ('Frozen Paneer 200g', 110, 0.08)
        ],
        'brands': ['Amul', 'Kwality Walls', 'Vadilal', 'McCain'],
        'seasonal_boost': {'Summer': 1.6, 'Winter': 0.7},
        'weather_impact': {'Sunny': 1.4, 'Rainy': 0.8},
        'is_perishable': True,
        'avg_expiry_days': 90
    }
}

# Create weighted product catalog
products_catalog = []
product_id = 1
for category, details in categories.items():
    for product_name, base_price, popularity in details['products']:
        products_catalog.append({
            'product_id': f'PRD_{product_id:05d}',
            'product_name': product_name,
            'category': category,
            'base_price': base_price,
            'popularity': popularity,
            'brands': details['brands'],
            'seasonal_boost': details.get('seasonal_boost', {}),
            'weather_impact': details.get('weather_impact', {}),
            'is_perishable': details['is_perishable'],
            'avg_expiry_days': details.get('avg_expiry_days', None)
        })
        product_id += 1

# Customer behavior profiles
customer_profiles = {
    'Premium': {
        'avg_basket_size': 20,
        'basket_std': 8,
        'visit_frequency_days': 7,
        'price_sensitivity': 0.3,
        'organic_preference': 0.6,
        'loyalty_engagement': 0.8,
        'premium_brand_prob': 0.7
    },
    'Regular': {
        'avg_basket_size': 12,
        'basket_std': 5,
        'visit_frequency_days': 4,
        'price_sensitivity': 0.5,
        'organic_preference': 0.3,
        'loyalty_engagement': 0.6,
        'premium_brand_prob': 0.4
    },
    'Occasional': {
        'avg_basket_size': 6,
        'basket_std': 3,
        'visit_frequency_days': 14,
        'price_sensitivity': 0.7,
        'organic_preference': 0.1,
        'loyalty_engagement': 0.2,
        'premium_brand_prob': 0.2
    },
    'New': {
        'avg_basket_size': 8,
        'basket_std': 4,
        'visit_frequency_days': 10,
        'price_sensitivity': 0.6,
        'organic_preference': 0.2,
        'loyalty_engagement': 0.1,
        'premium_brand_prob': 0.3
    }
}

# Time-based patterns
time_slots = {
    'Early Morning (6-9 AM)': {'hours': (6, 9), 'traffic': 0.10, 'avg_basket': 8, 'categories': ['Bakery', 'Dairy Products', 'Beverages']},
    'Morning (9-12 PM)': {'hours': (9, 12), 'traffic': 0.20, 'avg_basket': 15, 'categories': ['Fresh Produce', 'Dairy Products', 'Staples & Grains']},
    'Afternoon (12-4 PM)': {'hours': (12, 16), 'traffic': 0.15, 'avg_basket': 10, 'categories': ['Snacks & Confectionery', 'Beverages']},
    'Evening (4-9 PM)': {'hours': (16, 21), 'traffic': 0.45, 'avg_basket': 18, 'categories': ['Fresh Produce', 'Cooking Essentials', 'Household Items']},
    'Night (9-11 PM)': {'hours': (21, 23), 'traffic': 0.10, 'avg_basket': 6, 'categories': ['Snacks & Confectionery', 'Beverages']}
}

# Date setup
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

indian_holidays = [
    '2022-01-26', '2022-03-18', '2022-04-14', '2022-05-03', '2022-08-15', '2022-08-31',
    '2022-10-05', '2022-10-24', '2022-11-08', '2022-12-25',
    '2023-01-26', '2023-03-08', '2023-04-14', '2023-05-05', '2023-08-15', '2023-09-19',
    '2023-10-02', '2023-10-24', '2023-11-12', '2023-12-25'
]
holiday_dates = set([datetime.strptime(d, '%Y-%m-%d').date() for d in indian_holidays])

seasons = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Summer',
           6: 'Summer', 7: 'Monsoon', 8: 'Monsoon', 9: 'Monsoon',
           10: 'Winter', 11: 'Winter', 12: 'Winter'}

# ============================================================================
# GENERATE REALISTIC TRANSACTIONS
# ============================================================================

print("Generating transactions with realistic patterns...")
print("- Seasonal variations in product demand")
print("- Weather impact on sales")
print("- Customer loyalty and shopping patterns")
print("- Time-of-day preferences")
print("- Price sensitivity and promotions")
print()

transactions_data = []
transaction_id = 1

# Create customer base with shopping history
num_customers = 200000
customer_last_visit = {}

BATCH_SIZE = 100000
NUM_BATCHES = 20

for batch_num in range(NUM_BATCHES):
    print(f"Batch {batch_num + 1}/{NUM_BATCHES}...", end=' ')

    for i in range(BATCH_SIZE):
        # Select date with realistic distribution
        trans_date = random.choice(date_range)
        is_weekend = trans_date.weekday() >= 5
        is_holiday = trans_date.date() in holiday_dates
        season = seasons[trans_date.month]

        # More transactions on weekends and holidays
        if is_holiday:
            if random.random() > 0.3:  # 70% chance to proceed
                pass
            else:
                continue
        elif is_weekend:
            if random.random() > 0.2:  # 80% chance
                pass
            else:
                continue

        # Select time slot with realistic distribution
        time_slot_name = random.choices(
            list(time_slots.keys()),
            weights=[slot['traffic'] for slot in time_slots.values()]
        )[0]
        time_slot_info = time_slots[time_slot_name]

        hour = random.randint(time_slot_info['hours'][0], time_slot_info['hours'][1] - 1)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        timestamp = trans_date.replace(hour=hour, minute=minute, second=second)

        # Select store
        store = random.choice(stores_lookup)

        # Select customer with realistic behavior
        customer_id = f'CUST_{random.randint(1, num_customers):06d}'

        # Customer type influences shopping frequency
        if customer_id in customer_last_visit:
            days_since_last = (trans_date - customer_last_visit[customer_id]).days
            # Regular customers more likely
            if days_since_last < 3:
                customer_type = random.choice(['Regular', 'Premium'])
            else:
                customer_type = random.choices(
                    ['Regular', 'Premium', 'Occasional', 'New'],
                    weights=[0.40, 0.10, 0.40, 0.10]
                )[0]
        else:
            customer_type = random.choices(
                ['Regular', 'Premium', 'Occasional', 'New'],
                weights=[0.30, 0.10, 0.40, 0.20]
            )[0]

        customer_last_visit[customer_id] = trans_date
        profile = customer_profiles[customer_type]

        # Demographics
        age_group = random.choices(
            ['18-25', '26-35', '36-45', '46-60', '60+'],
            weights=[0.10, 0.35, 0.30, 0.20, 0.05]
        )[0]
        gender = random.choices(['Male', 'Female', 'Other'], weights=[0.48, 0.50, 0.02])[0]

        # Basket size influenced by time, customer type, and day type
        base_basket = int(np.random.normal(profile['avg_basket_size'], profile['basket_std']))
        basket_multiplier = 1.3 if (is_weekend or is_holiday) else 1.0
        basket_size = max(1, int(base_basket * basket_multiplier))

        # Select product with realistic preferences
        # Time slot influences product category
        if random.random() < 0.6:  # 60% influenced by time
            preferred_categories = time_slot_info['categories']
            product = random.choice([p for p in products_catalog if p['category'] in preferred_categories])
        else:
            # Weighted by popularity
            product = random.choices(products_catalog, weights=[p['popularity'] for p in products_catalog])[0]

        # Quantity based on product type
        if product['category'] in ['Staples & Grains', 'Household Items']:
            quantity = random.randint(1, 3)
        elif product['category'] in ['Fresh Produce', 'Dairy Products']:
            quantity = random.randint(1, 5)
        else:
            quantity = random.randint(1, min(8, basket_size))

        # Brand selection based on customer profile
        if random.random() < profile['premium_brand_prob']:
            brand = product['brands'][0] if len(product['brands']) > 0 else 'Local'
        else:
            brand = random.choice(product['brands'])

        sub_category = random.choices(
            ['Premium', 'Regular', 'Economy', 'Organic'],
            weights=[profile['premium_brand_prob'], 0.4, 0.3, profile['organic_preference']]
        )[0]

        # Pricing with realistic factors
        base_price = product['base_price']

        # Store tier affects pricing
        store_price = base_price * store['price_multiplier']

        # Seasonal pricing
        seasonal_factor = product['seasonal_boost'].get(season, 1.0)

        # Weather impact
        if season == 'Monsoon':
            weather = random.choices(['Rainy', 'Cloudy', 'Sunny', 'Stormy'], weights=[0.5, 0.3, 0.15, 0.05])[0]
        elif season == 'Summer':
            weather = random.choices(['Sunny', 'Cloudy', 'Rainy', 'Stormy'], weights=[0.7, 0.2, 0.08, 0.02])[0]
        else:
            weather = random.choices(['Sunny', 'Cloudy', 'Rainy', 'Stormy'], weights=[0.5, 0.35, 0.12, 0.03])[0]

        weather_factor = product['weather_impact'].get(weather, 1.0)

        # Premium/Economy adjustment
        if sub_category == 'Premium':
            price_adjustment = 1.25
        elif sub_category == 'Economy':
            price_adjustment = 0.85
        elif sub_category == 'Organic':
            price_adjustment = 1.4
        else:
            price_adjustment = 1.0

        unit_price = round(store_price * seasonal_factor * price_adjustment, 2)

        # Discount logic - more aggressive on weekends, holidays, and for price-sensitive customers
        base_discount = 0
        if is_holiday:
            base_discount = random.choice([10, 15, 20, 25, 30])
        elif is_weekend:
            base_discount = random.choice([0, 5, 10, 15])
        elif random.random() < 0.3:
            base_discount = random.choice([0, 5, 10])

        # Perishable items near expiry get higher discounts
        if product['is_perishable']:
            days_to_expiry = random.randint(1, product['avg_expiry_days'])
            if days_to_expiry <= 2:
                base_discount = max(base_discount, 30)
            elif days_to_expiry <= 5:
                base_discount = max(base_discount, 15)
        else:
            days_to_expiry = None

        # Customer sensitivity affects response to discounts
        if base_discount > 0 and random.random() > profile['price_sensitivity']:
            quantity = min(10, int(quantity * 1.5))  # Buy more on discount

        discount_percentage = base_discount
        final_price = unit_price * (1 - discount_percentage / 100)
        total_amount = round(quantity * final_price, 2)

        # Loyalty points
        loyalty_balance = random.randint(100, 5000) if random.random() < profile['loyalty_engagement'] else 0
        loyalty_points_used = random.randint(0, min(200, loyalty_balance)) if loyalty_balance > 50 and random.random() > 0.6 else 0
        loyalty_points_earned = int(total_amount * 0.02) if customer_type in ['Premium', 'Regular'] else int(total_amount * 0.01)

        # Promotion
        promotion_id = f'PROMO_{random.randint(1, 50):03d}' if discount_percentage > 15 else None

        # Temperature based on season
        if season == 'Summer':
            temperature = random.randint(28, 42)
        elif season == 'Winter':
            temperature = random.randint(12, 25)
        elif season == 'Monsoon':
            temperature = random.randint(22, 32)
        else:
            temperature = random.randint(20, 30)

        # Payment method - UPI more popular now
        payment_method = random.choices(
            ['UPI', 'Card', 'Cash', 'Wallet', 'Credit'],
            weights=[0.45, 0.25, 0.15, 0.10, 0.05]
        )[0]

        # Delivery method
        delivery_method = random.choices(
            ['In-store', 'Home Delivery', 'Click & Collect'],
            weights=[0.75, 0.20, 0.05]
        )[0]

        # Operational details
        stock_level = random.randint(10, 1000)
        checkout_duration = random.randint(45, 180) if basket_size < 10 else random.randint(120, 400)
        shelf_location = f'Aisle {random.randint(1, 20)}' if random.random() > 0.15 else random.choice(['End Cap', 'Promo Display', 'Front Display'])

        transactions_data.append({
            'transaction_id': f'TXN_{transaction_id:015d}',
            'timestamp': timestamp,
            'store_id': store['store_id'],
            'store_region': store['region'],
            'store_type': store['store_type'],
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'category': product['category'],
            'sub_category': sub_category,
            'brand': brand,
            'quantity': quantity,
            'unit_price': unit_price,
            'discount_percentage': discount_percentage,
            'final_price': round(final_price, 2),
            'total_amount': total_amount,
            'payment_method': payment_method,
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
            'delivery_method': delivery_method,
            'time_slot': time_slot_name,
            'employee_id': f'EMP_{random.randint(1, 500):03d}',
            'checkout_duration_sec': checkout_duration,
            'origin_country': random.choice(['India', 'USA', 'Thailand', 'Australia']) if product['category'] in ['Fresh Produce'] else 'India',
            'is_organic': sub_category == 'Organic',
            'shelf_location': shelf_location
        })

        transaction_id += 1

    print(f"✓ {len(transactions_data):,} transactions generated")

print(f"\n{'='*80}")
print("Creating DataFrame and exporting...")

df = pd.DataFrame(transactions_data)

print(f"\nDataset Summary:")
print(f"{'='*80}")
print(f"Total Transactions: {len(df):,}")
print(f"Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Total Revenue: ₹{df['total_amount'].sum():,.2f}")
print(f"Average Transaction: ₹{df['total_amount'].mean():.2f}")
print(f"Median Transaction: ₹{df['total_amount'].median():.2f}")
print(f"Unique Customers: {df['customer_id'].nunique():,}")
print(f"Unique Products: {df['product_id'].nunique():,}")
print(f"\nCustomer Distribution:")
for ctype in df['customer_type'].unique():
    count = len(df[df['customer_type'] == ctype])
    pct = count / len(df) * 100
    print(f"  {ctype}: {count:,} ({pct:.1f}%)")

print(f"\nExporting to CSV...")
df.to_csv('grocery_dataset.csv', index=False)

print(f"\n{'='*80}")
print("✓ REALISTIC DATASET GENERATION COMPLETE!")
print(f"{'='*80}")
print(f"\nFile: grocery_dataset.csv")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"{'='*80}")
