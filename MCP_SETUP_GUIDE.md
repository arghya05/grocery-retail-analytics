# 🚀 Grocery Analytics MCP Server - Setup Guide

## ✅ What's Been Set Up

Your grocery store data is now in PostgreSQL with a fully functional MCP server that allows you to query insights using natural language!

### 📊 Database Status
- **Database Name**: `grocery_analytics`
- **Total Records**: 1,869,621 transactions
- **Total Revenue**: ₹682,281,733.16
- **Date Range**: January 2022 - December 2023
- **Unique Customers**: 199,981
- **Unique Products**: 59

### 🗄️ Database Structure

#### Main Table: `transactions`
Contains all 1.87M transactions with 39 columns including:
- Transaction details (ID, timestamp, amount)
- Store information (ID, region, type)
- Product details (ID, name, category, brand, pricing)
- Customer information (ID, type, demographics, loyalty)
- Operational data (payment method, delivery, checkout time)
- External factors (weather, season, temperature)

#### Materialized Views (Pre-computed Analytics)
For lightning-fast queries:
- `daily_sales_summary` - Daily aggregated metrics
- `category_performance` - Category-level analysis
- `top_products` - Product performance rankings
- `customer_insights` - Customer segmentation
- `store_performance` - Store-level metrics

### 🛠️ MCP Server Tools

The MCP server provides 10 powerful tools:

#### 1. **get_sales_summary**
Get overall business metrics
```
Total revenue, transactions, avg transaction value, items sold, customers
```

#### 2. **get_top_products**
Find best-selling products
```
Parameters:
  - limit: Number of products (default: 10)
  - order_by: 'revenue' or 'quantity'
```

#### 3. **get_category_performance**
Analyze category-level performance
```
Revenue, transactions, units sold by category
```

#### 4. **get_customer_insights**
Customer segmentation analysis
```
Parameters:
  - segment: 'Regular', 'Premium', 'Occasional', 'New', or 'all'
```

#### 5. **get_store_performance**
Store-level metrics
```
Parameters:
  - store_id: Specific store or 'all'
  - limit: Number of stores to return
```

#### 6. **get_seasonal_analysis**
Seasonal performance trends
```
Revenue and transactions by season (Winter/Summer/Monsoon/Spring)
```

#### 7. **get_daily_sales_trend**
Daily sales over time
```
Parameters:
  - start_date: YYYY-MM-DD
  - end_date: YYYY-MM-DD
```

#### 8. **get_payment_method_analysis**
Payment preferences and trends
```
Transactions and revenue by payment method (UPI/Card/Cash/etc)
```

#### 9. **get_hourly_traffic_pattern**
Traffic and revenue by time of day
```
Busiest hours, revenue patterns, checkout times
```

#### 10. **execute_custom_query**
Run custom SQL queries
```
Parameters:
  - query: SELECT statement for advanced analysis
```

---

## 🎯 How to Use

### Option 1: Direct Database Queries

Connect to PostgreSQL:
```bash
psql -d grocery_analytics
```

Example queries:
```sql
-- Total revenue
SELECT SUM(total_amount) FROM transactions;

-- Top 10 products
SELECT * FROM top_products LIMIT 10;

-- Category performance
SELECT * FROM category_performance;

-- Customer segmentation
SELECT customer_type, COUNT(*), SUM(lifetime_value)
FROM customer_insights
GROUP BY customer_type;
```

### Option 2: Use Claude Code with MCP

The MCP server is at: `/Users/arghya.mukherjee/Downloads/cursor/sd/grocery_mcp_server.py`

#### In Claude Code:
Simply ask natural language questions like:

```
"Show me the top 10 products by revenue"
"What's the sales summary?"
"Analyze customer segments"
"Which season has the highest revenue?"
"Show store performance for all stores"
```

The MCP server will automatically query the database and format results.

### Option 3: Command Line MCP Testing

Test individual tools:
```bash
cd /Users/arghya.mukherjee/Downloads/cursor/sd

# Make script executable
chmod +x grocery_mcp_server.py

# The MCP server runs via stdio
# It's designed to be called by MCP-compatible clients (like Claude Code)
```

---

## 📈 Sample Insights You Can Get

### Business Questions → MCP Tools

| Question | Tool to Use | Example |
|----------|-------------|---------|
| What's my total revenue? | `get_sales_summary` | Overall business metrics |
| Which products sell best? | `get_top_products` | Top 10 by revenue or quantity |
| How do categories perform? | `get_category_performance` | Revenue % by category |
| Who are my VIP customers? | `get_customer_insights` | Premium customer analysis |
| Which stores underperform? | `get_store_performance` | Bottom 5 stores |
| Is summer better than winter? | `get_seasonal_analysis` | Seasonal comparison |
| What are peak shopping hours? | `get_hourly_traffic_pattern` | Traffic by time |
| Is UPI popular? | `get_payment_method_analysis` | Payment preferences |
| How did last month perform? | `get_daily_sales_trend` | Specific date range |
| Custom analysis? | `execute_custom_query` | Your own SQL |

---

## 🔧 Advanced Usage

### Refreshing Materialized Views

When you add new data, refresh the pre-computed views:

```sql
REFRESH MATERIALIZED VIEW daily_sales_summary;
REFRESH MATERIALIZED VIEW category_performance;
REFRESH MATERIALIZED VIEW top_products;
REFRESH MATERIALIZED VIEW customer_insights;
REFRESH MATERIALIZED VIEW store_performance;
```

Or refresh all at once:
```bash
psql -d grocery_analytics -c "REFRESH MATERIALIZED VIEW daily_sales_summary; REFRESH MATERIALIZED VIEW category_performance; REFRESH MATERIALIZED VIEW top_products; REFRESH MATERIALIZED VIEW customer_insights; REFRESH MATERIALIZED VIEW store_performance;"
```

### Custom SQL Queries

Complex analysis examples:

```sql
-- Revenue by day of week
SELECT
    EXTRACT(DOW FROM timestamp) as day_of_week,
    TO_CHAR(timestamp, 'Day') as day_name,
    COUNT(*) as transactions,
    SUM(total_amount) as revenue
FROM transactions
GROUP BY day_of_week, day_name
ORDER BY day_of_week;

-- Customer lifetime value buckets
SELECT
    CASE
        WHEN lifetime_value < 500 THEN '< ₹500'
        WHEN lifetime_value < 1000 THEN '₹500-1,000'
        WHEN lifetime_value < 5000 THEN '₹1,000-5,000'
        ELSE '> ₹5,000'
    END as ltv_bucket,
    COUNT(*) as customer_count,
    SUM(lifetime_value) as total_revenue
FROM customer_insights
GROUP BY ltv_bucket
ORDER BY MIN(lifetime_value);

-- Products with highest discount
SELECT
    product_name,
    category,
    AVG(discount_percentage) as avg_discount,
    COUNT(*) as times_discounted
FROM transactions
WHERE discount_percentage > 0
GROUP BY product_name, category
ORDER BY avg_discount DESC
LIMIT 20;

-- Peak hours by day type
SELECT
    CASE
        WHEN is_weekend THEN 'Weekend'
        WHEN is_holiday THEN 'Holiday'
        ELSE 'Weekday'
    END as day_type,
    time_slot,
    COUNT(*) as transactions,
    AVG(total_amount) as avg_transaction
FROM transactions
GROUP BY day_type, time_slot
ORDER BY day_type, transactions DESC;
```

---

## 🚨 Troubleshooting

### Issue: "Database connection failed"
**Solution**: Check PostgreSQL is running:
```bash
pg_ctl status
# or
brew services list | grep postgresql
```

Start if needed:
```bash
brew services start postgresql@14
```

### Issue: "Permission denied"
**Solution**: Update DB_PARAMS in `grocery_mcp_server.py` with your username:
```python
DB_PARAMS = {
    'dbname': 'grocery_analytics',
    'user': 'YOUR_USERNAME',  # Update this
    'password': '',
    'host': 'localhost',
    'port': '5432'
}
```

### Issue: "Materialized view doesn't exist"
**Solution**: Re-run the data loading script:
```bash
python load_data_to_postgres.py
```

---

## 📊 Performance Tips

### 1. Use Materialized Views
For frequently accessed data, query the materialized views instead of the main table:
- ✅ `SELECT * FROM top_products LIMIT 10` (Fast)
- ❌ `SELECT ... FROM transactions GROUP BY ...` (Slow for 1.87M rows)

### 2. Use Indexes
All common query patterns have indexes:
- timestamp, store_id, product_id, customer_id, category, etc.

### 3. Limit Results
Always use LIMIT for large result sets:
```sql
SELECT * FROM transactions LIMIT 1000;
```

### 4. Filter Early
Use WHERE clauses to reduce data:
```sql
SELECT * FROM transactions
WHERE timestamp >= '2023-01-01'
  AND category = 'Beverages'
LIMIT 100;
```

---

## 📁 File Structure

```
/Users/arghya.mukherjee/Downloads/cursor/sd/
├── grocery_dataset.csv           # Original CSV data (525 MB)
├── load_data_to_postgres.py      # Database setup script
├── grocery_mcp_server.py          # MCP server (main file)
├── mcp_config.json                # MCP configuration
├── setup_postgres_db.sql          # SQL schema (reference)
├── COMPLETE_DATA_INSIGHTS.md      # Full insights report
├── STORE_MANAGER_ACTION_PLAN.md   # Business recommendations
└── MCP_SETUP_GUIDE.md             # This file
```

---

## 🎓 Next Steps

### 1. **Explore the Data**
Try different MCP tools to understand your business:
```
"Show me seasonal analysis"
"What are the top 20 products?"
"Compare customer segments"
```

### 2. **Build Dashboards**
Use the MCP tools to create real-time dashboards:
- Sales KPIs
- Customer segments
- Product performance
- Store rankings

### 3. **Automate Reports**
Schedule queries for daily/weekly reports:
```bash
# Daily sales report
psql -d grocery_analytics -c "SELECT * FROM daily_sales_summary WHERE sale_date = CURRENT_DATE;"
```

### 4. **Advanced Analytics**
Use custom queries for:
- Market basket analysis
- Customer churn prediction
- Demand forecasting
- Price optimization

---

## 💡 Example Use Cases

### For Store Managers
```
"Which products are running low on stock?"
"Show me today's sales performance"
"Which stores need attention?"
"What's the busiest hour today?"
```

### For Marketing Teams
```
"Who are our VIP customers?"
"Which customer segment should we target?"
"What's the impact of promotions?"
"Which products have highest loyalty?"
```

### For Finance Teams
```
"What's the monthly revenue trend?"
"Show category profitability"
"Analyze payment method costs"
"Calculate customer lifetime value"
```

### For Operations Teams
```
"What are peak shopping hours?"
"Show checkout efficiency by store"
"Analyze delivery method preferences"
"Which products cause delays?"
```

---

## 🔐 Security Notes

- The MCP server only allows SELECT queries for security
- No write operations via MCP (use direct psql for data updates)
- Database credentials stored locally (not exposed)
- Consider adding password protection for production use

---

## 📞 Support

### Quick Reference
- Database: `psql -d grocery_analytics`
- MCP Server: `/Users/arghya.mukherjee/Downloads/cursor/sd/grocery_mcp_server.py`
- Insights Report: `COMPLETE_DATA_INSIGHTS.md`
- Action Plan: `STORE_MANAGER_ACTION_PLAN.md`

### Common Commands
```bash
# Check database
psql -d grocery_analytics -c "\dt"

# View data sample
psql -d grocery_analytics -c "SELECT * FROM transactions LIMIT 5;"

# Check views
psql -d grocery_analytics -c "\dm"

# Database size
psql -d grocery_analytics -c "SELECT pg_size_pretty(pg_database_size('grocery_analytics'));"
```

---

## ✅ Summary

You now have:
- ✅ **1.87M transactions** loaded in PostgreSQL
- ✅ **10 MCP tools** for instant insights
- ✅ **Pre-computed views** for fast analytics
- ✅ **Complete documentation** for all use cases

**You're ready to query your grocery store data with natural language using the MCP server!** 🎉

---

*Last Updated: October 2024*
*Database: grocery_analytics | PostgreSQL 14*
