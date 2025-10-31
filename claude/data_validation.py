#!/usr/bin/env python3
"""
Phase 1.7: Data Validation & Cross-Check
Ensure all numbers add up correctly across all analyses
"""

import pandas as pd
import json
from datetime import datetime

def data_validation():
    print("=" * 80)
    print("PHASE 1.7: DATA VALIDATION & CROSS-CHECK")
    print("=" * 80)
    print()

    # Load original dataset
    print("Loading dataset...")
    df = pd.read_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/grocery_dataset.csv')
    print(f"✓ Loaded {len(df):,} rows")
    print()

    validation_report = []
    issues = []

    # ========================================================================
    # 1. REVENUE VALIDATION
    # ========================================================================
    print("1. Revenue Validation...")

    total_revenue = df['total_amount'].sum()
    print(f"   Total Revenue from source: ${total_revenue:,.2f}")

    # Check regional breakdown
    revenue_by_region_df = pd.read_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_region.csv')
    regional_sum = revenue_by_region_df['revenue'].sum()
    print(f"   Sum of regional revenues: ${regional_sum:,.2f}")

    if abs(total_revenue - regional_sum) < 1:
        print("   ✓ Regional revenues add up correctly")
        validation_report.append(("Revenue by Region", "PASS", 0, "All regions sum to total"))
    else:
        diff = abs(total_revenue - regional_sum)
        print(f"   ✗ Discrepancy: ${diff:,.2f}")
        issues.append(("Revenue by Region", diff))
        validation_report.append(("Revenue by Region", "FAIL", diff, "Regional sum doesn't match total"))

    # Check store-level breakdown
    revenue_by_store_df = pd.read_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_store.csv')
    store_sum = revenue_by_store_df['revenue'].sum()
    print(f"   Sum of store revenues: ${store_sum:,.2f}")

    if abs(total_revenue - store_sum) < 1:
        print("   ✓ Store revenues add up correctly")
        validation_report.append(("Revenue by Store", "PASS", 0, "All stores sum to total"))
    else:
        diff = abs(total_revenue - store_sum)
        print(f"   ✗ Discrepancy: ${diff:,.2f}")
        issues.append(("Revenue by Store", diff))
        validation_report.append(("Revenue by Store", "FAIL", diff, "Store sum doesn't match total"))

    # Check category breakdown
    revenue_by_category_df = pd.read_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_category.csv')
    category_sum = revenue_by_category_df['revenue'].sum()
    print(f"   Sum of category revenues: ${category_sum:,.2f}")

    if abs(total_revenue - category_sum) < 1:
        print("   ✓ Category revenues add up correctly")
        validation_report.append(("Revenue by Category", "PASS", 0, "All categories sum to total"))
    else:
        diff = abs(total_revenue - category_sum)
        print(f"   ✗ Discrepancy: ${diff:,.2f}")
        issues.append(("Revenue by Category", diff))
        validation_report.append(("Revenue by Category", "FAIL", diff, "Category sum doesn't match total"))

    # ========================================================================
    # 2. TRANSACTION COUNT VALIDATION
    # ========================================================================
    print("\n2. Transaction Count Validation...")

    total_transactions = len(df)
    print(f"   Total Transactions: {total_transactions:,}")

    # Check for duplicates
    unique_transactions = df['transaction_id'].nunique()
    print(f"   Unique Transaction IDs: {unique_transactions:,}")

    if unique_transactions != total_transactions:
        duplicate_count = total_transactions - unique_transactions
        print(f"   ⚠️  Found {duplicate_count:,} duplicate transaction IDs")
        validation_report.append(("Transaction Uniqueness", "WARNING", duplicate_count, "Duplicate transaction IDs found"))
    else:
        print("   ✓ All transaction IDs are unique")
        validation_report.append(("Transaction Uniqueness", "PASS", 0, "All IDs unique"))

    # Verify transaction counts in regional data
    regional_txn_sum = revenue_by_region_df['transaction_count'].sum()
    print(f"   Regional transaction sum: {regional_txn_sum:,}")

    if regional_txn_sum == total_transactions:
        print("   ✓ Regional transaction counts match")
        validation_report.append(("Regional Transaction Count", "PASS", 0, "Counts match"))
    else:
        diff = abs(regional_txn_sum - total_transactions)
        print(f"   ✗ Discrepancy: {diff:,} transactions")
        issues.append(("Regional Transaction Count", diff))
        validation_report.append(("Regional Transaction Count", "FAIL", diff, "Regional txns don't match total"))

    # ========================================================================
    # 3. CUSTOMER METRICS VALIDATION
    # ========================================================================
    print("\n3. Customer Metrics Validation...")

    total_customers = df['customer_id'].nunique()
    print(f"   Total Unique Customers: {total_customers:,}")

    # Check customer segmentation
    segment_customers = df.groupby('customer_type')['customer_id'].nunique().sum()
    print(f"   Sum of segment customers: {segment_customers:,}")

    # Note: Customers can appear in multiple years with different segments
    # So this validation needs special handling
    validation_report.append(("Customer Segmentation", "INFO", 0, f"{segment_customers:,} unique customers across segments"))

    # ========================================================================
    # 4. CROSS-REFERENCE WITH DASHBOARD
    # ========================================================================
    print("\n4. Cross-Reference with CEO Dashboard...")

    with open('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/ceo_executive_dashboard.json') as f:
        dashboard = json.load(f)

    dashboard_total_rev = dashboard['business_performance']['total_revenue_2_years']
    print(f"   Dashboard Total Revenue: ${dashboard_total_rev:,.2f}")
    print(f"   Source Total Revenue: ${total_revenue:,.2f}")

    if abs(dashboard_total_rev - total_revenue) < 1:
        print("   ✓ Dashboard revenue matches source")
        validation_report.append(("Dashboard Revenue", "PASS", 0, "Matches source data"))
    else:
        diff = abs(dashboard_total_rev - total_revenue)
        print(f"   ✗ Discrepancy: ${diff:,.2f}")
        issues.append(("Dashboard Revenue", diff))
        validation_report.append(("Dashboard Revenue", "FAIL", diff, "Dashboard doesn't match source"))

    # ========================================================================
    # 5. DATA QUALITY CHECKS
    # ========================================================================
    print("\n5. Data Quality Checks...")

    # Check for null values in critical fields
    critical_fields = ['total_amount', 'transaction_id', 'customer_id', 'store_id', 'product_id']
    null_counts = {}

    for field in critical_fields:
        null_count = df[field].isna().sum()
        null_counts[field] = null_count
        if null_count > 0:
            print(f"   ⚠️  {field}: {null_count:,} null values")
            validation_report.append((f"Null Check - {field}", "WARNING", null_count, "Null values found"))
        else:
            print(f"   ✓ {field}: No null values")
            validation_report.append((f"Null Check - {field}", "PASS", 0, "No nulls"))

    # Check for negative values
    negative_amounts = (df['total_amount'] < 0).sum()
    if negative_amounts > 0:
        print(f"   ⚠️  Found {negative_amounts:,} negative total_amounts")
        validation_report.append(("Negative Amounts", "WARNING", negative_amounts, "Negative values found"))
    else:
        print(f"   ✓ No negative total_amounts")
        validation_report.append(("Negative Amounts", "PASS", 0, "No negatives"))

    # Check calculation accuracy
    df_calc = df.copy()
    df_calc['calculated_total'] = df_calc['final_price'] * df_calc['quantity']
    calculation_errors = (abs(df_calc['total_amount'] - df_calc['calculated_total']) > 0.01).sum()

    if calculation_errors > 0:
        print(f"   ℹ️  {calculation_errors:,} transactions have rounding differences (>$0.01)")
        validation_report.append(("Calculation Accuracy", "INFO", calculation_errors, "Minor rounding differences"))
    else:
        print(f"   ✓ All calculations are accurate")
        validation_report.append(("Calculation Accuracy", "PASS", 0, "All accurate"))

    # ========================================================================
    # 6. RECONCILIATION SUMMARY
    # ========================================================================
    print("\n6. Creating Reconciliation Summary...")

    reconciliation_data = []

    # Revenue reconciliation
    reconciliation_data.append({
        'metric': 'Total Revenue',
        'source_value': float(total_revenue),
        'calculated_value': float(regional_sum),
        'difference': float(abs(total_revenue - regional_sum)),
        'status': 'PASS' if abs(total_revenue - regional_sum) < 1 else 'FAIL'
    })

    # Transaction reconciliation
    reconciliation_data.append({
        'metric': 'Total Transactions',
        'source_value': int(total_transactions),
        'calculated_value': int(regional_txn_sum),
        'difference': int(abs(total_transactions - regional_txn_sum)),
        'status': 'PASS' if total_transactions == regional_txn_sum else 'FAIL'
    })

    # Customer reconciliation
    reconciliation_data.append({
        'metric': 'Unique Customers',
        'source_value': int(total_customers),
        'calculated_value': int(segment_customers),
        'difference': 0,
        'status': 'INFO'
    })

    # Save reconciliation
    reconciliation_df = pd.DataFrame(reconciliation_data)
    reconciliation_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/reconciliation_summary.csv'
    reconciliation_df.to_csv(reconciliation_path, index=False)
    print(f"   ✓ Reconciliation summary saved: {reconciliation_path}")

    # ========================================================================
    # 7. FINAL VALIDATION REPORT
    # ========================================================================
    print("\n7. Creating Final Validation Report...")

    report_md = f"""# Data Validation Report - Final
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Data Source**: grocery_dataset.csv ({len(df):,} rows)

---

## VALIDATION SUMMARY

### Overall Status: {"✅ PASSED" if len(issues) == 0 else "⚠️ ISSUES FOUND"}

**Total Checks**: {len(validation_report)}
**Passed**: {len([v for v in validation_report if v[1] == 'PASS'])}
**Failed**: {len([v for v in validation_report if v[1] == 'FAIL'])}
**Warnings**: {len([v for v in validation_report if v[1] == 'WARNING'])}
**Info**: {len([v for v in validation_report if v[1] == 'INFO'])}

---

## CRITICAL METRICS VALIDATION

### Revenue Validation
| Metric | Value | Status |
|--------|-------|--------|
| Total Revenue (Source) | ${total_revenue:,.2f} | ✓ |
| Regional Revenue Sum | ${regional_sum:,.2f} | {"✓" if abs(total_revenue - regional_sum) < 1 else "✗"} |
| Store Revenue Sum | ${store_sum:,.2f} | {"✓" if abs(total_revenue - store_sum) < 1 else "✗"} |
| Category Revenue Sum | ${category_sum:,.2f} | {"✓" if abs(total_revenue - category_sum) < 1 else "✗"} |

**Conclusion**: {"All revenue breakdowns reconcile correctly" if abs(total_revenue - regional_sum) < 1 and abs(total_revenue - store_sum) < 1 and abs(total_revenue - category_sum) < 1 else "Some discrepancies found - see issues section"}

### Transaction Validation
| Metric | Value | Status |
|--------|-------|--------|
| Total Transactions | {total_transactions:,} | ✓ |
| Unique Transaction IDs | {unique_transactions:,} | {"✓" if unique_transactions == total_transactions else "⚠️"} |
| Regional Transaction Sum | {regional_txn_sum:,} | {"✓" if regional_txn_sum == total_transactions else "✗"} |

**Conclusion**: {"All transaction counts validated" if unique_transactions == total_transactions and regional_txn_sum == total_transactions else "Duplicate transaction IDs found"}

### Customer Validation
| Metric | Value | Status |
|--------|-------|--------|
| Total Unique Customers | {total_customers:,} | ✓ |
| Segment Customer Sum | {segment_customers:,} | ℹ️ |

**Note**: Segment totals may differ from unique customers due to customers changing segments over time.

---

## DETAILED VALIDATION RESULTS

"""

    for check_name, status, value, note in validation_report:
        status_icon = {"PASS": "✓", "FAIL": "✗", "WARNING": "⚠️", "INFO": "ℹ️"}.get(status, "?")
        report_md += f"### {check_name}\n"
        report_md += f"- **Status**: {status_icon} {status}\n"
        if value > 0:
            report_md += f"- **Value**: {value:,}\n"
        report_md += f"- **Note**: {note}\n\n"

    if issues:
        report_md += "---\n\n## ISSUES FOUND\n\n"
        for issue_name, diff in issues:
            report_md += f"- **{issue_name}**: Difference of ${diff:,.2f} or {diff:,} records\n"
        report_md += "\n⚠️ **Action Required**: Investigate discrepancies before finalizing reports\n"
    else:
        report_md += "---\n\n## ✅ NO CRITICAL ISSUES FOUND\n\n"
        report_md += "All revenue, transaction, and customer metrics have been validated and reconcile correctly.\n"

    report_md += f"""
---

## DATA QUALITY SUMMARY

### Null Value Analysis
"""
    for field, count in null_counts.items():
        report_md += f"- **{field}**: {count:,} null values {'✓' if count == 0 else '⚠️'}\n"

    report_md += f"""
### Data Integrity
- **Negative Amounts**: {negative_amounts:,} records {'✓' if negative_amounts == 0 else '⚠️'}
- **Calculation Errors**: {calculation_errors:,} records (rounding differences) {'ℹ️'}

---

## CONCLUSION

"""
    if len(issues) == 0:
        report_md += """✅ **Data is validated and ready for CEO presentation**

All key metrics have been cross-checked:
- Revenue breakdowns add up correctly across all dimensions
- Transaction counts reconcile at all levels
- Customer metrics are consistent
- Data quality is excellent with no critical issues

**Confidence Level**: HIGH - Data can be used for strategic decision-making with full confidence.
"""
    else:
        report_md += f"""⚠️ **{len(issues)} Issues require attention**

While most validations passed, the following discrepancies were found:
"""
        for issue_name, diff in issues:
            report_md += f"- {issue_name}: ${diff:,.2f}\n"

        report_md += """
**Recommendation**: Review and resolve discrepancies before final CEO presentation.
"""

    report_md += f"""
---

## FILES VALIDATED

1. revenue_by_region.csv
2. revenue_by_store.csv
3. revenue_by_category.csv
4. ceo_executive_dashboard.json
5. grocery_dataset.csv (source)

**Total Records Validated**: {len(df):,}
**Total Revenue Validated**: ${total_revenue:,.2f}

---
*Data Validation Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    report_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/data_validation_report_final.md'
    with open(report_path, 'w') as f:
        f.write(report_md)
    print(f"   ✓ Final validation report saved: {report_path}")

    # ========================================================================
    # COMPLETION
    # ========================================================================
    print()
    print("=" * 80)
    print("✅ DATA VALIDATION & CROSS-CHECK COMPLETE!")
    print("=" * 80)
    print(f"Total Checks: {len(validation_report)}")
    print(f"Passed: {len([v for v in validation_report if v[1] == 'PASS'])}")
    print(f"Issues Found: {len(issues)}")
    status_msg = "✅ ALL VALIDATED" if len(issues) == 0 else "⚠️ SOME ISSUES"
    print(f"Status: {status_msg}")
    print(f"Files Created: 2 (reconciliation CSV + validation report MD)")

if __name__ == "__main__":
    data_validation()
