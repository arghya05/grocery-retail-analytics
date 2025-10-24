# Grocery Store Manager Insights Dataset Plan
## 20 Lakh (2,000,000) Rows

---

## Executive Summary
This dataset is designed to provide comprehensive insights for grocery store managers, covering sales transactions, inventory management, customer behavior, and operational efficiency across multiple dimensions.

---

## 1. Dataset Schema

### Main Transaction Table (2,000,000 rows)

| Column Name | Data Type | Description | Sample Values |
|-------------|-----------|-------------|---------------|
| **transaction_id** | VARCHAR(20) | Unique transaction identifier | TXN_2024001234567 |
| **timestamp** | DATETIME | Transaction date and time | 2024-01-15 14:23:45 |
| **store_id** | VARCHAR(10) | Store location identifier | STR_001 to STR_050 |
| **store_region** | VARCHAR(20) | Geographic region | North, South, East, West, Central |
| **store_type** | VARCHAR(20) | Store format | Supermarket, Hypermarket, Express |
| **product_id** | VARCHAR(15) | Product SKU | PRD_001 to PRD_500 |
| **product_name** | VARCHAR(100) | Product description | Basmati Rice 5kg, Milk 1L, etc. |
| **category** | VARCHAR(30) | Main category | Dairy, Grains, Vegetables, Fruits, Snacks, Beverages, etc. |
| **sub_category** | VARCHAR(30) | Sub-category | Organic, Premium, Regular, Economy |
| **brand** | VARCHAR(50) | Brand name | Mother Dairy, Amul, Fortune, Tata, Local, etc. |
| **quantity** | INTEGER | Units sold | 1-20 |
| **unit_price** | DECIMAL(10,2) | Price per unit (INR) | 10.00 - 5000.00 |
| **discount_percentage** | DECIMAL(5,2) | Discount applied | 0-50% |
| **final_price** | DECIMAL(10,2) | After discount | Calculated |
| **total_amount** | DECIMAL(10,2) | quantity × final_price | Calculated |
| **payment_method** | VARCHAR(20) | Payment type | Cash, Card, UPI, Wallet, Credit |
| **customer_id** | VARCHAR(15) | Customer identifier | CUST_000001 to CUST_200000 |
| **customer_type** | VARCHAR(20) | Customer segment | Regular, Premium, New, Occasional |
| **loyalty_points_used** | INTEGER | Points redeemed | 0-1000 |
| **loyalty_points_earned** | INTEGER | Points earned | 0-500 |
| **age_group** | VARCHAR(20) | Customer age bracket | 18-25, 26-35, 36-45, 46-60, 60+ |
| **gender** | VARCHAR(10) | Customer gender | Male, Female, Other |
| **basket_size** | INTEGER | Items in transaction | 1-50 |
| **is_weekend** | BOOLEAN | Weekend indicator | TRUE/FALSE |
| **is_holiday** | BOOLEAN | Holiday indicator | TRUE/FALSE |
| **season** | VARCHAR(15) | Season | Summer, Monsoon, Winter, Spring |
| **promotion_id** | VARCHAR(15) | Active promotion | PROMO_001 or NULL |
| **stock_level_at_sale** | INTEGER | Inventory after sale | 0-1000 |
| **supplier_id** | VARCHAR(15) | Product supplier | SUP_001 to SUP_100 |
| **days_to_expiry** | INTEGER | Perishable shelf life | 1-365 or NULL |
| **weather_condition** | VARCHAR(20) | Weather during sale | Sunny, Rainy, Cloudy, Stormy |
| **temperature_celsius** | INTEGER | Temperature | 15-45 |
| **delivery_method** | VARCHAR(20) | Fulfillment type | In-store, Home Delivery, Click & Collect |
| **time_slot** | VARCHAR(20) | Time of day | Early Morning, Morning, Afternoon, Evening, Night |
| **employee_id** | VARCHAR(15) | Cashier/staff ID | EMP_001 to EMP_500 |
| **checkout_duration_sec** | INTEGER | Transaction time | 30-600 seconds |
| **origin_country** | VARCHAR(30) | Product origin | India, USA, Thailand, etc. |
| **is_organic** | BOOLEAN | Organic certification | TRUE/FALSE |
| **shelf_location** | VARCHAR(30) | Store placement | Aisle 1-20, End Cap, Promo Display |

---

## 2. Data Distribution Strategy

### 2.1 Temporal Distribution (2 million rows)
- **Date Range**: 2 years (730 days)
- **Average**: ~2,740 transactions per day
- **Peak Days**: Weekends (3,500-4,500 transactions)
- **Weekdays**: 2,000-3,000 transactions
- **Festivals/Holidays**: 5,000-8,000 transactions
- **Monthly Patterns**: Higher in festival months (Oct-Nov, Mar-Apr)

### 2.2 Store Distribution (50 stores)
- **Metro Stores** (15 stores): 60% of transactions
- **Tier-2 Cities** (20 stores): 30% of transactions
- **Tier-3 Cities** (15 stores): 10% of transactions
- **Store Types**:
  - Hypermarkets (10): 50% transactions
  - Supermarkets (30): 40% transactions
  - Express Stores (10): 10% transactions

### 2.3 Product Distribution (500 unique SKUs)

#### Category Breakdown:
1. **Staples & Grains** (20%): Rice, wheat, flour, pulses
2. **Dairy Products** (15%): Milk, yogurt, cheese, butter
3. **Fresh Produce** (12%): Vegetables, fruits
4. **Beverages** (10%): Tea, coffee, juices, soft drinks
5. **Snacks & Confectionery** (10%): Chips, biscuits, chocolates
6. **Cooking Essentials** (8%): Oil, spices, condiments
7. **Personal Care** (8%): Soap, shampoo, toothpaste
8. **Household Items** (7%): Detergents, cleaners
9. **Bakery** (5%): Bread, buns, cakes
10. **Frozen Foods** (5%): Ice cream, frozen vegetables

### 2.4 Customer Distribution (200,000 unique customers)
- **Regular Customers** (30%): 60% of transactions
- **Occasional Customers** (50%): 30% of transactions
- **New Customers** (20%): 10% of transactions

**Demographics**:
- Age 26-35: 35%
- Age 36-45: 30%
- Age 46-60: 20%
- Age 18-25: 10%
- Age 60+: 5%

---

## 3. Key Insights Enabled

### 3.1 Sales Analytics
- Revenue trends by time, store, category
- Best and worst-performing products
- Sales velocity and turnover rates
- Seasonality patterns
- Festival vs. regular day performance
- Hour-of-day demand patterns

### 3.2 Customer Behavior
- Purchase frequency and recency
- Customer lifetime value (CLV)
- Basket analysis (market basket)
- Customer segmentation (RFM analysis)
- Loyalty program effectiveness
- Cross-selling opportunities
- Customer churn prediction

### 3.3 Inventory Management
- Stock turnover rates
- Slow-moving vs. fast-moving items
- Optimal reorder points
- Wastage for perishables (days to expiry)
- Stockout incidents
- Supplier performance

### 3.4 Pricing & Promotions
- Price elasticity analysis
- Discount effectiveness
- Promotion ROI
- Competitive pricing insights
- Bundle opportunities

### 3.5 Operational Efficiency
- Peak hour staffing needs
- Checkout duration optimization
- Employee performance metrics
- Store layout effectiveness
- Delivery method preferences

### 3.6 External Factors
- Weather impact on sales
- Holiday/event-driven demand
- Regional preferences
- Seasonal product performance

---

## 4. Data Generation Rules

### 4.1 Realistic Constraints
1. **Basket Coherence**: Related products in same transaction
2. **Price Ranges**: Category-appropriate pricing
3. **Discount Logic**: Higher discounts on slow-moving items
4. **Time Patterns**: Peak hours (6-9 AM, 5-9 PM)
5. **Perishable Logic**: Shorter expiry = higher discounts
6. **Customer Behavior**: Regular customers have higher basket sizes
7. **Geographic Variance**: Regional product preferences
8. **Seasonal Relevance**: Ice cream higher in summer, etc.

### 4.2 Data Quality Rules
- **No Missing Critical Fields**: transaction_id, timestamp, product_id
- **Referential Integrity**: Valid FK relationships
- **Business Logic**: final_price ≤ unit_price
- **Reasonable Ranges**: All values within realistic bounds
- **Date Continuity**: No gaps in operational dates

---

## 5. Implementation Plan

### Phase 1: Schema Setup
1. Create database tables
2. Define indexes (transaction_id, timestamp, customer_id, product_id)
3. Set up constraints and relationships

### Phase 2: Reference Data (Master Tables)
1. **Stores Table** (50 records)
2. **Products Table** (500 records)
3. **Customers Table** (200,000 records)
4. **Employees Table** (500 records)
5. **Suppliers Table** (100 records)
6. **Promotions Table** (50 records)

### Phase 3: Transaction Data Generation
1. Generate 2M rows with realistic distributions
2. Apply business rules and constraints
3. Validate data quality

### Phase 4: Data Validation
1. Check distributions match specifications
2. Verify no orphan records
3. Test query performance
4. Generate summary statistics

---

## 6. Technology Stack Options

### Option 1: Python-based Generation
- **Libraries**: Faker, NumPy, Pandas
- **Database**: PostgreSQL, MySQL
- **Storage**: CSV, Parquet, Database

### Option 2: Cloud-based
- **AWS**: RDS, S3, Glue
- **Azure**: SQL Database, Data Factory
- **GCP**: BigQuery, Cloud Storage

### Option 3: Big Data Tools
- **Apache Spark**: For large-scale generation
- **Databricks**: Unified platform

---

## 7. Sample Queries for Insights

```sql
-- Top 10 Products by Revenue
SELECT product_name, SUM(total_amount) as revenue
FROM transactions
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 10;

-- Customer Segmentation (RFM)
SELECT customer_id,
       MAX(timestamp) as last_purchase,
       COUNT(*) as frequency,
       SUM(total_amount) as monetary_value
FROM transactions
GROUP BY customer_id;

-- Hourly Sales Pattern
SELECT time_slot, AVG(total_amount) as avg_revenue
FROM transactions
GROUP BY time_slot
ORDER BY avg_revenue DESC;

-- Category Performance by Season
SELECT category, season, SUM(total_amount) as revenue
FROM transactions
GROUP BY category, season;

-- Weather Impact Analysis
SELECT weather_condition, AVG(basket_size), SUM(total_amount)
FROM transactions
GROUP BY weather_condition;
```

---

## 8. Expected File Size

- **CSV Format**: ~500-700 MB
- **Parquet Format**: ~150-250 MB (compressed)
- **Database**: ~1-1.5 GB (with indexes)

---

## 9. Deliverables

1. **Master Data Files**
   - stores.csv
   - products.csv
   - customers.csv
   - employees.csv
   - suppliers.csv

2. **Transaction Data**
   - transactions.csv (or parquet)
   - OR Database dump

3. **Documentation**
   - Data dictionary
   - Generation script
   - Sample queries
   - Insights dashboard (optional)

4. **Validation Report**
   - Row count verification
   - Distribution checks
   - Data quality metrics

---

## 10. Timeline Estimate

- **Week 1**: Schema finalization & master data creation
- **Week 2**: Transaction generation logic & testing
- **Week 3**: Full dataset generation & validation
- **Week 4**: Documentation & delivery

---

## 11. Use Cases for Store Manager

1. **Daily Operations**: Staffing decisions, stock replenishment
2. **Strategic Planning**: Product mix optimization, store expansion
3. **Marketing**: Targeted promotions, customer retention
4. **Procurement**: Supplier negotiations, inventory optimization
5. **Financial**: Revenue forecasting, budget planning
6. **Competitive Analysis**: Pricing strategies, market positioning

---

## Next Steps

1. Review and approve this plan
2. Choose technology stack
3. Begin implementation
4. Iterative validation
5. Final delivery

---

**Document Version**: 1.0  
**Created**: October 15, 2024  
**Author**: Dataset Planning Team

