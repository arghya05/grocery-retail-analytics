-- Create database for grocery store data
DROP DATABASE IF EXISTS grocery_analytics;
CREATE DATABASE grocery_analytics;

-- Connect to the database
\c grocery_analytics

-- Create main transactions table
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
);

-- Create indexes for common queries
CREATE INDEX idx_timestamp ON transactions(timestamp);
CREATE INDEX idx_store_id ON transactions(store_id);
CREATE INDEX idx_product_id ON transactions(product_id);
CREATE INDEX idx_customer_id ON transactions(customer_id);
CREATE INDEX idx_category ON transactions(category);
CREATE INDEX idx_customer_type ON transactions(customer_type);
CREATE INDEX idx_season ON transactions(season);
CREATE INDEX idx_payment_method ON transactions(payment_method);
CREATE INDEX idx_date ON transactions(DATE(timestamp));

-- Create materialized views for common analytics

-- Daily sales summary
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT
    DATE(timestamp) as sale_date,
    COUNT(*) as total_transactions,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    SUM(quantity) as total_items_sold,
    COUNT(DISTINCT customer_id) as unique_customers
FROM transactions
GROUP BY DATE(timestamp)
ORDER BY sale_date;

CREATE INDEX idx_daily_sales_date ON daily_sales_summary(sale_date);

-- Category performance
CREATE MATERIALIZED VIEW category_performance AS
SELECT
    category,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    SUM(quantity) as total_units_sold,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM transactions), 2) as revenue_percentage
FROM transactions
GROUP BY category
ORDER BY total_revenue DESC;

-- Top products
CREATE MATERIALIZED VIEW top_products AS
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
ORDER BY total_revenue DESC;

-- Customer segmentation
CREATE MATERIALIZED VIEW customer_insights AS
SELECT
    customer_id,
    customer_type,
    age_group,
    gender,
    COUNT(*) as visit_count,
    SUM(total_amount) as lifetime_value,
    AVG(total_amount) as avg_transaction_value,
    AVG(basket_size) as avg_basket_size,
    MAX(timestamp) as last_visit,
    MIN(timestamp) as first_visit
FROM transactions
GROUP BY customer_id, customer_type, age_group, gender
ORDER BY lifetime_value DESC;

CREATE INDEX idx_customer_insights_type ON customer_insights(customer_type);
CREATE INDEX idx_customer_insights_ltv ON customer_insights(lifetime_value);

-- Store performance
CREATE MATERIALIZED VIEW store_performance AS
SELECT
    store_id,
    store_region,
    store_type,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(DISTINCT DATE(timestamp)) as active_days
FROM transactions
GROUP BY store_id, store_region, store_type
ORDER BY total_revenue DESC;

-- Hourly traffic pattern
CREATE MATERIALIZED VIEW hourly_traffic AS
SELECT
    time_slot,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    AVG(checkout_duration_sec) as avg_checkout_time,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as traffic_percentage
FROM transactions
GROUP BY time_slot
ORDER BY transaction_count DESC;

-- Seasonal analysis
CREATE MATERIALIZED VIEW seasonal_analysis AS
SELECT
    season,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    COUNT(DISTINCT customer_id) as unique_customers,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM transactions), 2) as revenue_percentage
FROM transactions
GROUP BY season
ORDER BY total_revenue DESC;

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON DATABASE grocery_analytics TO your_username;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_username;

COMMENT ON TABLE transactions IS 'Main grocery store transactions data from 2022-2023';
COMMENT ON MATERIALIZED VIEW daily_sales_summary IS 'Daily aggregated sales metrics';
COMMENT ON MATERIALIZED VIEW category_performance IS 'Product category performance analysis';
COMMENT ON MATERIALIZED VIEW top_products IS 'Top performing products by revenue';
COMMENT ON MATERIALIZED VIEW customer_insights IS 'Customer segmentation and lifetime value';
COMMENT ON MATERIALIZED VIEW store_performance IS 'Store-level performance metrics';
COMMENT ON MATERIALIZED VIEW hourly_traffic IS 'Hourly traffic patterns and revenue';
COMMENT ON MATERIALIZED VIEW seasonal_analysis IS 'Seasonal performance trends';
