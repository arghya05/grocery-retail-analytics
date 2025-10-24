#!/usr/bin/env python3
"""
Verify that all CSV files are being loaded by the enhanced assistant
"""

from store_manager_assistant_enhanced import EnhancedStoreManagerAssistant
import sys

print("\n" + "="*70)
print("VERIFYING ALL CSV FILES ARE LOADED")
print("="*70)

try:
    # Initialize assistant
    print("\nInitializing enhanced assistant...")
    assistant = EnhancedStoreManagerAssistant(model="llama3.2:1b")

    # Count loaded datasets
    kpi_count = len(assistant.context_data)
    print(f"\n✓ Total datasets loaded: {kpi_count}")

    # List all loaded datasets
    print("\nLoaded KPI Datasets:")
    for i, key in enumerate(sorted(assistant.context_data.keys()), 1):
        df = assistant.context_data[key]
        print(f"  {i:2d}. {key:25s} - {len(df):5d} rows")

    # Check for expected datasets
    expected = [
        'comprehensive_kpis',
        'overall_business',
        'store_performance',
        'category_performance',
        'product_performance',
        'customer_segment',
        'daily_performance',
        'weekly_performance',
        'monthly_performance',
        'payment_method',
        'time_slot',
        'delivery_method',
        'weekend_weekday',
        'age_group',
        'gender',
        'seasonal',
        'brand_performance',
        'organic_vs_nonorganic',
        'employee_performance',
        'master_dashboard'
    ]

    missing = [e for e in expected if e not in assistant.context_data]

    if missing:
        print(f"\n⚠️  Missing {len(missing)} expected datasets:")
        for m in missing:
            print(f"  - {m}")
    else:
        print(f"\n✅ ALL {len(expected)} EXPECTED DATASETS LOADED!")

    # Check business context
    if assistant.business_context:
        print(f"\n✓ Business context metadata loaded")
        print(f"  - {len(assistant.business_context)} intelligence sections")
        for key in assistant.business_context.keys():
            print(f"    • {key}")
    else:
        print("\n⚠️  Business context metadata not loaded")

    # Check insights document
    if assistant.insights_document:
        print(f"\n✓ Complete data insights document loaded")
        print(f"  - {len(assistant.insights_document)} characters")
        print(f"  - {assistant.insights_document.count('===')} sections")
    else:
        print("\n⚠️  Insights document not loaded")

    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)

    print(f"\n📊 Summary:")
    print(f"  • KPI Datasets: {kpi_count}")
    print(f"  • Business Context: {'✓ Loaded' if assistant.business_context else '✗ Missing'}")
    print(f"  • Insights Document: {'✓ Loaded' if assistant.insights_document else '✗ Missing'}")

    if not missing and assistant.business_context and assistant.insights_document:
        print(f"\n🎉 ALL DATA SOURCES SUCCESSFULLY LOADED!")
        print(f"   The assistant has complete context from all CSV files plus metadata.")
    else:
        print(f"\n⚠️  Some data sources are missing. Check file paths.")

except Exception as e:
    print(f"\n❌ Verification failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
