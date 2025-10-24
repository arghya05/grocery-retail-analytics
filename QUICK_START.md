# 🚀 Grocery Analytics - Quick Start

## ✅ Setup Complete!

Your grocery store data is now in PostgreSQL with an MCP server ready to use!

---

## 📊 What You Have

| Component | Status | Details |
|-----------|--------|---------|
| **PostgreSQL Database** | ✅ Running | `grocery_analytics` database |
| **Data Loaded** | ✅ Complete | 1,869,621 transactions |
| **MCP Server** | ✅ Ready | 10 tools available |
| **Materialized Views** | ✅ Created | Fast pre-computed analytics |

---

## 🎯 Quick Access

### 1. Query Database Directly
```bash
psql -d grocery_analytics
```

Then run queries:
```sql
-- Total revenue
SELECT SUM(total_amount) FROM transactions;

-- Top products
SELECT * FROM top_products LIMIT 10;

-- Customer segmentation
SELECT * FROM customer_insights LIMIT 10;
```

### 2. Use the MCP Server

The MCP server is at:
```
/Users/arghya.mukherjee/Downloads/cursor/sd/grocery_mcp_server.py
```

**10 Available Tools:**
1. `get_sales_summary` - Overall business metrics
2. `get_top_products` - Best sellers
3. `get_category_performance` - Category analysis
4. `get_customer_insights` - Customer segments
5. `get_store_performance` - Store rankings
6. `get_seasonal_analysis` - Seasonal trends
7. `get_daily_sales_trend` - Time series
8. `get_payment_method_analysis` - Payment preferences
9. `get_hourly_traffic_pattern` - Traffic patterns
10. `execute_custom_query` - Custom SQL

---

## 💬 Example Questions (via MCP)

Simply ask in natural language:

```
"Show me the sales summary"
"What are the top 10 products by revenue?"
"Analyze customer segments"
"Which season has highest revenue?"
"Show me hourly traffic patterns"
"Get store performance for all stores"
```

The MCP server will query the database and return formatted results!

---

## 📈 Quick Database Stats

```
Total Transactions:   1,869,621
Total Revenue:        ₹682,281,733.16
Unique Customers:     199,981
Unique Products:      59
Active Stores:        50
Date Range:           Jan 2022 - Dec 2023
```

---

## 📁 Key Files

```
grocery_dataset.csv                - Original CSV (525 MB)
grocery_mcp_server.py              - MCP server
load_data_to_postgres.py           - Database loader
mcp_config.json                    - MCP configuration
MCP_SETUP_GUIDE.md                 - Full documentation
COMPLETE_DATA_INSIGHTS.md          - Business insights
STORE_MANAGER_ACTION_PLAN.md       - Action plan
```

---

## 🔥 Most Useful Queries

### Business Overview
```sql
SELECT * FROM daily_sales_summary ORDER BY sale_date DESC LIMIT 7;
```

### Top 10 Products
```sql
SELECT product_name, total_revenue, total_units_sold
FROM top_products LIMIT 10;
```

### Customer Segments
```sql
SELECT customer_type, COUNT(*) as count,
       AVG(lifetime_value) as avg_ltv
FROM customer_insights
GROUP BY customer_type
ORDER BY avg_ltv DESC;
```

### Store Rankings
```sql
SELECT store_id, total_revenue, transaction_count
FROM store_performance
ORDER BY total_revenue DESC;
```

### Seasonal Trends
```sql
SELECT season, SUM(total_amount) as revenue,
       COUNT(*) as transactions
FROM transactions
GROUP BY season
ORDER BY revenue DESC;
```

---

## 🛠️ Maintenance Commands

### Refresh Analytics (after new data)
```bash
psql -d grocery_analytics -c "
  REFRESH MATERIALIZED VIEW daily_sales_summary;
  REFRESH MATERIALIZED VIEW category_performance;
  REFRESH MATERIALIZED VIEW top_products;
  REFRESH MATERIALIZED VIEW customer_insights;
  REFRESH MATERIALIZED VIEW store_performance;
"
```

### Check Database Size
```bash
psql -d grocery_analytics -c "SELECT pg_size_pretty(pg_database_size('grocery_analytics'));"
```

### Backup Database
```bash
pg_dump grocery_analytics > grocery_analytics_backup.sql
```

---

## 📖 Full Documentation

Read `MCP_SETUP_GUIDE.md` for:
- Detailed tool descriptions
- Advanced SQL examples
- Troubleshooting
- Performance tips
- Security notes

---

## 🎉 You're Ready!

The MCP server enables you to **query your grocery data using natural language** through Claude Code!

Just ask questions and the MCP tools will fetch insights from your PostgreSQL database.

---

*Setup Date: October 2024*
*MCP Version: 1.0.0*
