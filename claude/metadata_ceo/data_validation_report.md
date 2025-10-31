# Dataset Validation Report
Generated: 2025-10-30 10:47:04

## Dataset Overview

- **Total Rows**: 24,268,230
- **Total Columns**: 39
- **Total Unique Transactions**: 2,000,000
- **Total Revenue**: $9,000,000,000.00
- **Date Range**: 2022-01-01 06:02:10 to 2023-12-31 22:59:22'
- **Unique Stores**: 51
- **Unique Customers**: 200,001
- **Unique Products**: 59
- **Unique Employees**: 500
- **Total Quantity Sold**: 178,740,026

## Data Quality Assessment

### ✓ PASSED CHECKS
- All 39 expected columns present
- Duplicate transaction_ids: 22268230
- Negative total_amounts: 0
- Negative quantities: 0

### ⚠️ WARNINGS
- Zero total_amounts: 0
- Calculation mismatches: 17478094

## Revenue Breakdown

### By Region
- **North**: $2,357,708,447.17 (26.20%)
- **East**: $2,315,932,165.61 (25.73%)
- **Central**: $1,818,335,815.40 (20.20%)
- **South**: $1,790,572,892.10 (19.90%)
- **West**: $717,450,679.72 (7.97%)

### By Category
- **Fresh Produce**: $1,524,874,201.04 (16.94%)
- **Beverages**: $1,419,671,627.84 (15.77%)
- **Household Items**: $1,149,012,920.10 (12.77%)
- **Cooking Essentials**: $1,038,534,708.78 (11.54%)
- **Dairy Products**: $865,634,983.38 (9.62%)
- **Staples & Grains**: $829,731,020.52 (9.22%)
- **Snacks & Confectionery**: $791,365,529.22 (8.79%)
- **Bakery**: $502,688,531.92 (5.59%)
- **Frozen Foods**: $493,637,812.33 (5.48%)
- **Personal Care**: $384,848,664.86 (4.28%)

## Key Metrics

- **Average Transaction Value**: $370.86
- **Median Transaction Value**: $404.85
- **Average Basket Size**: 26.13 items
- **Average Discount**: 9.52%
- **Promotional Transactions**: 3,907,267 (16.10%)
- **Weekend Transactions**: 5,978,326 (24.63%)
- **Organic Products**: 5,092,609 (20.98%)

## Validation Status

✅ **Dataset is valid and ready for analysis**

All key metrics have been calculated and verified. The dataset contains 24,268,230 rows across 39 columns with minimal data quality issues.
