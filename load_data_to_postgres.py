import pandas as pd
import psycopg2
from psycopg2 import sql
import sys
from io import StringIO

print("=" * 80)
print("LOADING GROCERY DATA INTO POSTGRESQL")
print("=" * 80)

# Database connection parameters
DB_PARAMS = {
    'dbname': 'grocery_analytics',
    'user': 'arghya.mukherjee',  # Update this to your PostgreSQL username
    'password': '',  # Add password if needed
    'host': 'localhost',
    'port': '5432'
}

print("\n[1/4] Reading CSV file...")
try:
    df = pd.read_csv('grocery_dataset.csv')
    print(f"   ✓ Loaded {len(df):,} transactions from CSV")
    print(f"   ✓ Columns: {len(df.columns)}")
except Exception as e:
    print(f"   ✗ Error reading CSV: {e}")
    sys.exit(1)

print("\n[2/4] Preprocessing data...")
# Convert boolean columns
df['is_weekend'] = df['is_weekend'].map({True: 't', False: 'f', 'True': 't', 'False': 'f'})
df['is_holiday'] = df['is_holiday'].map({True: 't', False: 'f', 'True': 't', 'False': 'f'})
df['is_organic'] = df['is_organic'].map({True: 't', False: 'f', 'True': 't', 'False': 'f'})

# Handle NaN values
df['promotion_id'] = df['promotion_id'].fillna('')
df['days_to_expiry'] = df['days_to_expiry'].fillna(0).astype(int)

print("   ✓ Data preprocessed")

print("\n[3/4] Connecting to PostgreSQL...")
try:
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    print("   ✓ Connected to database")
except Exception as e:
    print(f"   ✗ Connection failed: {e}")
    print("\n   Trying to create database first...")
    try:
        # Connect to default postgres database to create our database
        default_params = DB_PARAMS.copy()
        default_params['dbname'] = 'postgres'
        conn = psycopg2.connect(**default_params)
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='grocery_analytics'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE grocery_analytics")
            print("   ✓ Created database 'grocery_analytics'")

        cursor.close()
        conn.close()

        # Now connect to our database
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        print("   ✓ Connected to grocery_analytics database")
    except Exception as e2:
        print(f"   ✗ Failed to create/connect to database: {e2}")
        sys.exit(1)

print("\n[4/4] Loading data into PostgreSQL...")
print("   This may take a few minutes for 1.87M rows...")

try:
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id VARCHAR(20) PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            store_id VARCHAR(10) NOT NULL,
            store_region VARCHAR(20),
            store_type VARCHAR(20),
            product_id VARCHAR(15) NOT NULL,
            product_name VARCHAR(100),
            category VARCHAR(30),
            sub_category VARCHAR(30),
            brand VARCHAR(50),
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            discount_percentage DECIMAL(5,2),
            final_price DECIMAL(10,2),
            total_amount DECIMAL(10,2),
            payment_method VARCHAR(20),
            customer_id VARCHAR(15),
            customer_type VARCHAR(20),
            loyalty_points_used INTEGER,
            loyalty_points_earned INTEGER,
            age_group VARCHAR(20),
            gender VARCHAR(10),
            basket_size INTEGER,
            is_weekend BOOLEAN,
            is_holiday BOOLEAN,
            season VARCHAR(15),
            promotion_id VARCHAR(15),
            stock_level_at_sale INTEGER,
            supplier_id VARCHAR(15),
            days_to_expiry INTEGER,
            weather_condition VARCHAR(20),
            temperature_celsius INTEGER,
            delivery_method VARCHAR(20),
            time_slot VARCHAR(30),
            employee_id VARCHAR(15),
            checkout_duration_sec INTEGER,
            origin_country VARCHAR(30),
            is_organic BOOLEAN,
            shelf_location VARCHAR(30)
        )
    """)
    print("   ✓ Table created/verified")

    # Use COPY for fast bulk insert
    print("   ⏳ Inserting data using COPY command...")

    # Prepare data for COPY
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False, na_rep='\\N')
    buffer.seek(0)

    # Execute COPY
    cursor.copy_expert(
        "COPY transactions FROM STDIN WITH CSV NULL '\\N'",
        buffer
    )

    conn.commit()
    print(f"   ✓ Loaded {len(df):,} transactions successfully!")

    # Create indexes
    print("\n   Creating indexes...")
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_timestamp ON transactions(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_store_id ON transactions(store_id)",
        "CREATE INDEX IF NOT EXISTS idx_product_id ON transactions(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_customer_id ON transactions(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_category ON transactions(category)",
        "CREATE INDEX IF NOT EXISTS idx_customer_type ON transactions(customer_type)",
        "CREATE INDEX IF NOT EXISTS idx_season ON transactions(season)",
        "CREATE INDEX IF NOT EXISTS idx_date ON transactions(DATE(timestamp))",
    ]

    for idx_sql in indexes:
        cursor.execute(idx_sql)

    conn.commit()
    print("   ✓ Indexes created")

    # Create materialized views
    print("\n   Creating materialized views for fast analytics...")

    # Daily sales summary
    cursor.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS daily_sales_summary AS
        SELECT
            DATE(timestamp) as sale_date,
            COUNT(*) as total_transactions,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_transaction_value,
            SUM(quantity) as total_items_sold,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM transactions
        GROUP BY DATE(timestamp)
        ORDER BY sale_date
    """)

    # Category performance
    cursor.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS category_performance AS
        SELECT
            category,
            COUNT(*) as transaction_count,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_transaction_value,
            SUM(quantity) as total_units_sold,
            ROUND(CAST(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM transactions) AS NUMERIC), 2) as revenue_percentage
        FROM transactions
        GROUP BY category
        ORDER BY total_revenue DESC
    """)

    # Top products
    cursor.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS top_products AS
        SELECT
            product_id,
            product_name,
            category,
            brand,
            COUNT(*) as transaction_count,
            SUM(quantity) as total_units_sold,
            SUM(total_amount) as total_revenue,
            AVG(unit_price) as avg_unit_price,
            AVG(discount_percentage) as avg_discount
        FROM transactions
        GROUP BY product_id, product_name, category, brand
        ORDER BY total_revenue DESC
    """)

    # Store performance
    cursor.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS store_performance AS
        SELECT
            store_id,
            store_region,
            store_type,
            COUNT(*) as transaction_count,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_transaction_value,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM transactions
        GROUP BY store_id, store_region, store_type
        ORDER BY total_revenue DESC
    """)

    conn.commit()
    print("   ✓ Materialized views created")

    # Verify data
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)

    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    print(f"\n✓ Total transactions in database: {count:,}")

    cursor.execute("SELECT SUM(total_amount) FROM transactions")
    total_revenue = cursor.fetchone()[0]
    print(f"✓ Total revenue: ₹{float(total_revenue):,.2f}")

    cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM transactions")
    customers = cursor.fetchone()[0]
    print(f"✓ Unique customers: {customers:,}")

    cursor.execute("SELECT COUNT(DISTINCT product_id) FROM transactions")
    products = cursor.fetchone()[0]
    print(f"✓ Unique products: {products}")

    print("\n" + "=" * 80)
    print("✅ DATA LOADED SUCCESSFULLY!")
    print("=" * 80)
    print("\nYou can now query the database:")
    print("  psql -d grocery_analytics")
    print("\nOr use the MCP server (coming next!)")

except Exception as e:
    print(f"\n   ✗ Error loading data: {e}")
    conn.rollback()
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    cursor.close()
    conn.close()
    print("\n✓ Database connection closed")
