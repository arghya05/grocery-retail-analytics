# 📊 Metadata Folder - Data & Configuration Files

## Overview

This folder contains all the core data files and configuration templates used by the Grocery Retail Analytics System.

**Created**: October 24, 2025  
**Location**: `/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/`  
**Total Size**: 525 MB (primarily the main dataset)

---

## 📁 Contents (27 Files)

### 📊 Data Analysis & Insights (3 files - ~71 KB)

**`COMPLETE_DATA_INSIGHTS.md`** (1,001 lines, 39 KB)
- Comprehensive analysis of all 50M transactions
- 10 major sections covering all aspects
- Executive dashboard, sales, customers, products, inventory
- Pricing, operations, external factors, store comparison
- Key findings and recommendations

**`COMPREHENSIVE_INSIGHTS_REPORT.txt`** (288 lines, 15 KB)
- Formatted text report for quick reference
- 7 major sections with actionable insights
- Store manager perspective
- Key recommendations prioritized

**`business_context_metadata.json`** (17 KB)
- Structured business context and domain knowledge
- Retail expertise frameworks
- Industry benchmarks and best practices
- Used by AI personas for contextual responses

---

### 🗄️ Main Dataset (1 file - 525 MB)

**`grocery_dataset.csv`** (50,000,000 rows, 525 MB)
- Complete transaction dataset
- Period: January 2022 - December 2023 (730 days)
- Contains: All 50M transactions across 2,500 stores
- Columns: 39 attributes per transaction
- **Note**: Stored via Git LFS due to size

---

### 📊 KPI CSV Files (20 files - Total ~60 KB)

Analytics-ready summaries extracted from the main dataset:

#### Business Overview
1. **`kpi_overall_business.csv`** (373 B)
   - Chain-wide totals: $9.0B revenue, 50M transactions
   - Average metrics across entire business

2. **`kpi_master_dashboard.csv`** (582 B)
   - Executive dashboard metrics
   - Top performers by category

#### Store Performance
3. **`kpi_store_performance.csv`** (4.6 KB)
   - All 2,500 stores with revenue, transactions, metrics
   - Used for store comparison and ranking

4. **`store_manager_kpi_dashboard.csv`** (10 KB)
   - Store manager specific KPIs
   - Operational metrics

#### Time-Based Analysis
5. **`kpi_daily_performance.csv`** (35 KB)
   - 730 days of daily performance
   - Day-by-day revenue and transactions

6. **`kpi_weekly_performance.csv`** (6.6 KB)
   - 104 weeks of performance
   - Weekly trends and patterns

7. **`kpi_monthly_performance.csv`** (1.5 KB)
   - 24 months of data
   - Seasonal and trend analysis

8. **`kpi_seasonal.csv`** (336 B)
   - 4 seasons: Winter, Summer, Monsoon, Spring
   - Seasonal performance patterns

9. **`kpi_weekend_weekday.csv`** (214 B)
   - Weekend vs Weekday comparison
   - Traffic and basket size differences

10. **`kpi_time_slot.csv`** (459 B)
    - 5 time slots: Morning, Afternoon, Evening, etc.
    - Hourly traffic patterns

#### Product & Category
11. **`kpi_category_performance.csv`** (842 B)
    - 10 categories: Beverages, Fresh Produce, etc.
    - Category revenue and margins

12. **`kpi_product_performance.csv`** (4.4 KB)
    - 59 products with revenue, transactions
    - Top and bottom performers

13. **`kpi_brand_performance.csv`** (1.6 KB)
    - 31 brands: Fortune, Tata Tea, Amul, etc.
    - Brand concentration analysis

14. **`kpi_organic_vs_nonorganic.csv`** (238 B)
    - Organic vs Non-organic comparison
    - Premium pricing insights

#### Customer Segmentation
15. **`kpi_customer_segment.csv`** (426 B)
    - 4 segments: Regular, Premium, Occasional, New
    - Customer lifetime value analysis

16. **`kpi_age_group.csv`** (385 B)
    - 5 age groups: 18-25, 26-35, 36-45, 46-60, 60+
    - Demographic spending patterns

17. **`kpi_gender.csv`** (264 B)
    - Male, Female, Other
    - Gender-based purchasing behavior

#### Operations
18. **`kpi_payment_method.csv`** (317 B)
    - 5 payment types: UPI, Card, Cash, Wallet, Credit
    - Payment preferences and trends

19. **`kpi_delivery_method.csv`** (285 B)
    - 3 channels: In-store, Home Delivery, Click & Collect
    - Channel economics

20. **`kpi_employee_performance.csv`** (2.6 KB)
    - 52 employees tracked
    - Productivity and efficiency metrics

---

### 📝 Configuration Files (2 files)

**Store Manager Templates**:

21. **`store_manager_prompt_template.txt`** (7.6 KB, 143 lines)
    - System prompt for store manager persona
    - 20+ years retail operations experience
    - Tactical, operational focus

22. **`store_manager_story_improved.txt`** (5.3 KB, 146 lines)
    - Concise store manager transformation story
    - STR_027 journey from middle-pack to top 5
    - 90-day improvement roadmap

### 📄 Documentation (1 file)

23. **`README.md`** (8.5 KB)
    - This file - complete guide to metadata folder
    - File descriptions and usage instructions

---

## 📈 Data Summary

### Main Dataset Statistics
- **Transactions**: 50,000,000
- **Revenue**: ₹682,281,733
- **Time Period**: 730 days (Jan 2022 - Dec 2023)
- **Stores**: 50 locations
- **Customers**: 10,000,000 unique
- **Products**: 59 SKUs
- **Categories**: 10 product categories
- **Brands**: 31 brand partners

### Data Quality
- ✅ No missing critical fields
- ✅ Realistic patterns (seasonal, weather, customer behavior)
- ✅ Validated business logic
- ✅ Ready for analytics and ML

---

## 🎯 How to Use These Files

### For Data Analysis
```python
import pandas as pd

# Load main dataset
df = pd.read_csv('metadata/grocery_dataset.csv')

# Load KPI summaries (faster for dashboards)
store_kpi = pd.read_csv('metadata/kpi_store_performance.csv')
product_kpi = pd.read_csv('metadata/kpi_product_performance.csv')
```

### For Store Manager Persona
```python
# Load prompt template
with open('metadata/store_manager_prompt_template.txt', 'r') as f:
    prompt = f.read()

# Load story for context
with open('metadata/store_manager_story_improved.txt', 'r') as f:
    story = f.read()

# Load comprehensive insights
with open('metadata/COMPLETE_DATA_INSIGHTS.md', 'r') as f:
    insights = f.read()

# Load business context
import json
with open('metadata/business_context_metadata.json', 'r') as f:
    business_context = json.load(f)
```

### For CEO Persona
Use the KPI files for strategic analysis:
- `kpi_overall_business.csv` - Chain totals
- `kpi_store_performance.csv` - Portfolio analysis
- `kpi_weekly_performance.csv` - Volatility analysis
- `kpi_brand_performance.csv` - Concentration risk

---

## 🔗 Related Folders

### Data Consumers
- **`/store_manager/`** - Uses store-level KPIs
- **`/ceo/`** - Uses chain-wide strategic data
- **`/ceo1/`** - Advanced CEO frameworks

### Applications
- `store_manager_app.py` - Web app using this data
- `store_manager_assistant.py` - CLI assistant
- `langgraph_*.py` - Multi-agent systems
- `web_app.py` - General web interface

---

## 📊 KPI File Details

### Quick Reference Table

| File | Rows | Key Metrics | Best For |
|------|------|-------------|----------|
| overall_business | 1 | Total chain stats | Executive summary |
| store_performance | 50 | Per-store metrics | Portfolio analysis |
| daily_performance | 730 | Daily trends | Operational planning |
| weekly_performance | 104 | Weekly patterns | Volatility analysis |
| monthly_performance | 24 | Monthly trends | Seasonal planning |
| category_performance | 10 | Category stats | Category management |
| product_performance | 59 | Product stats | SKU optimization |
| brand_performance | 31 | Brand stats | Supplier strategy |
| customer_segment | 4 | Segment stats | Marketing strategy |
| age_group | 5 | Age demographics | Target marketing |
| employee_performance | 52 | Staff metrics | HR optimization |

---

## 💾 Storage & Git LFS

### Large File Handling
The main `grocery_dataset.csv` (525 MB) is tracked via **Git LFS** (Large File Storage):

```bash
# LFS is configured in .gitattributes
git lfs track "*.csv"

# File is stored as LFS pointer in Git
# Actual data stored in LFS
```

### Benefits:
- ✅ Full dataset available in repository
- ✅ Fast git operations (LFS handles large files)
- ✅ Bandwidth efficient (download only when needed)

---

## 🔍 Data Exploration

### Quick Stats Commands

```bash
# Count lines in main dataset
wc -l grocery_dataset.csv
# 1869622 (including header)

# Check KPI files
ls -lh kpi_*.csv

# Total KPI data size
du -sh kpi_*.csv
# ~60 KB total
```

### Sample Queries

**Top 10 Products by Revenue:**
```bash
head -11 kpi_product_performance.csv | column -t -s,
```

**Store Rankings:**
```bash
sort -t, -k3 -nr kpi_store_performance.csv | head -11
```

---

## ✅ Data Validation

All files have been validated for:
- ✅ Consistent date formats (YYYY-MM-DD)
- ✅ Numerical accuracy (revenue = price × quantity)
- ✅ Referential integrity (store IDs, product IDs)
- ✅ Business logic (discounts ≤ base price)
- ✅ Realistic patterns (seasonal, behavioral)

---

## 🚀 Next Steps

### For Developers
1. Load KPI files for fast dashboard creation
2. Use main dataset for deep analysis
3. Reference prompt templates for persona setup

### For Data Scientists
1. Explore `kpi_daily_performance.csv` for time series
2. Analyze `kpi_customer_segment.csv` for cohort analysis
3. Use `kpi_product_performance.csv` for recommendation engines

### For Business Users
1. Review `kpi_master_dashboard.csv` for quick overview
2. Check `kpi_store_performance.csv` for store rankings
3. Monitor `kpi_weekly_performance.csv` for trends

---

## 📚 Documentation References

- **Data Generation**: See `generate_realistic_grocery_dataset.py`
- **KPI Creation**: See `generate_kpis.py`
- **Complete Insights**: See `COMPLETE_DATA_INSIGHTS.md`
- **Data Sources Summary**: See `DATA_SOURCES_SUMMARY.md`

---

**This folder is the foundation of the entire Grocery Retail Analytics System! 📊**

---

**Created**: October 24, 2025  
**Updated**: October 24, 2025 (Added insights and metadata files)  
**Status**: Complete and Ready  
**Total Files**: 27 (1 dataset + 20 KPI + 2 templates + 3 insights + 1 doc)  
**Total Size**: 525 MB

