#!/usr/bin/env python3
"""
Phase 1.2A: Build Revenue Analysis Tree
Hierarchical breakdown: Total → Region → Store → Category → Sub-Category → Brand → SKU
"""

import pandas as pd
import json
from collections import defaultdict

def build_revenue_tree():
    print("=" * 80)
    print("PHASE 1.2A: BUILDING REVENUE ANALYSIS TREE")
    print("=" * 80)
    print()

    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/grocery_dataset.csv')
    print(f"✓ Loaded {len(df):,} rows")
    print()

    # Calculate total revenue
    total_revenue = df['total_amount'].sum()
    total_transactions = len(df)

    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Transactions: {total_transactions:,}")
    print()

    # Build hierarchical tree structure
    print("Building hierarchical revenue tree...")
    tree = {
        "total_revenue": float(total_revenue),
        "total_revenue_formatted": f"${total_revenue:,.2f}",
        "total_transactions": int(total_transactions),
        "avg_transaction_value": float(total_revenue / total_transactions),
        "breakdown": {}
    }

    # LEVEL 1: By Region
    print("\n" + "=" * 80)
    print("LEVEL 1: REVENUE BY REGION")
    print("=" * 80)

    region_data = df.groupby('store_region').agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    }).sort_values('total_amount', ascending=False)

    for region in region_data.index:
        region_df = df[df['store_region'] == region]
        rev = region_data.loc[region, 'total_amount']
        txn_count = region_data.loc[region, 'transaction_id']
        pct = (rev / total_revenue) * 100
        avg_txn = rev / txn_count

        print(f"{region:15s}: ${rev:15,.2f} ({pct:5.2f}%) | {txn_count:,} txns | Avg: ${avg_txn:.2f}")

        tree["breakdown"][region] = {
            "revenue": float(rev),
            "revenue_formatted": f"${rev:,.2f}",
            "percentage_of_total": float(pct),
            "transaction_count": int(txn_count),
            "avg_transaction_value": float(avg_txn),
            "stores": {}
        }

        # LEVEL 2: By Store (within region)
        print(f"\n  LEVEL 2: Stores in {region}")
        store_data = region_df.groupby('store_id').agg({
            'total_amount': 'sum',
            'transaction_id': 'count',
            'store_type': 'first'
        }).sort_values('total_amount', ascending=False)

        for store_id in store_data.index:
            store_df = region_df[region_df['store_id'] == store_id]
            store_rev = store_data.loc[store_id, 'total_amount']
            store_txn = store_data.loc[store_id, 'transaction_id']
            store_type = store_data.loc[store_id, 'store_type']
            store_pct = (store_rev / rev) * 100
            store_avg = store_rev / store_txn

            print(f"    {store_id:12s} ({store_type:12s}): ${store_rev:13,.2f} ({store_pct:5.2f}% of region)")

            tree["breakdown"][region]["stores"][store_id] = {
                "revenue": float(store_rev),
                "revenue_formatted": f"${store_rev:,.2f}",
                "percentage_of_region": float(store_pct),
                "percentage_of_total": float((store_rev / total_revenue) * 100),
                "transaction_count": int(store_txn),
                "avg_transaction_value": float(store_avg),
                "store_type": store_type,
                "categories": {}
            }

            # LEVEL 3: By Category (within store)
            category_data = store_df.groupby('category').agg({
                'total_amount': 'sum',
                'transaction_id': 'count'
            }).sort_values('total_amount', ascending=False)

            for category in category_data.index:
                cat_df = store_df[store_df['category'] == category]
                cat_rev = category_data.loc[category, 'total_amount']
                cat_pct = (cat_rev / store_rev) * 100

                tree["breakdown"][region]["stores"][store_id]["categories"][category] = {
                    "revenue": float(cat_rev),
                    "revenue_formatted": f"${cat_rev:,.2f}",
                    "percentage_of_store": float(cat_pct),
                    "percentage_of_total": float((cat_rev / total_revenue) * 100),
                    "subcategories": {}
                }

                # LEVEL 4: By Sub-Category (within category)
                subcat_data = cat_df.groupby('sub_category').agg({
                    'total_amount': 'sum',
                    'transaction_id': 'count'
                }).sort_values('total_amount', ascending=False)

                for subcat in subcat_data.index:
                    subcat_df = cat_df[cat_df['sub_category'] == subcat]
                    subcat_rev = subcat_data.loc[subcat, 'total_amount']
                    subcat_pct = (subcat_rev / cat_rev) * 100

                    tree["breakdown"][region]["stores"][store_id]["categories"][category]["subcategories"][subcat] = {
                        "revenue": float(subcat_rev),
                        "revenue_formatted": f"${subcat_rev:,.2f}",
                        "percentage_of_category": float(subcat_pct),
                        "percentage_of_total": float((subcat_rev / total_revenue) * 100),
                        "brands": {}
                    }

                    # LEVEL 5: By Brand (within sub-category)
                    brand_data = subcat_df.groupby('brand').agg({
                        'total_amount': 'sum',
                        'transaction_id': 'count'
                    }).sort_values('total_amount', ascending=False)

                    for brand in brand_data.index:
                        brand_df = subcat_df[subcat_df['brand'] == brand]
                        brand_rev = brand_data.loc[brand, 'total_amount']
                        brand_pct = (brand_rev / subcat_rev) * 100

                        tree["breakdown"][region]["stores"][store_id]["categories"][category]["subcategories"][subcat]["brands"][brand] = {
                            "revenue": float(brand_rev),
                            "revenue_formatted": f"${brand_rev:,.2f}",
                            "percentage_of_subcategory": float(brand_pct),
                            "percentage_of_total": float((brand_rev / total_revenue) * 100),
                            "products": {}
                        }

                        # LEVEL 6: By Product/SKU (within brand)
                        product_data = brand_df.groupby(['product_id', 'product_name']).agg({
                            'total_amount': 'sum',
                            'transaction_id': 'count',
                            'quantity': 'sum'
                        }).sort_values('total_amount', ascending=False)

                        for (prod_id, prod_name), row in product_data.iterrows():
                            prod_rev = row['total_amount']
                            prod_qty = row['quantity']
                            prod_pct = (prod_rev / brand_rev) * 100

                            tree["breakdown"][region]["stores"][store_id]["categories"][category]["subcategories"][subcat]["brands"][brand]["products"][prod_id] = {
                                "product_name": prod_name,
                                "revenue": float(prod_rev),
                                "revenue_formatted": f"${prod_rev:,.2f}",
                                "percentage_of_brand": float(prod_pct),
                                "percentage_of_total": float((prod_rev / total_revenue) * 100),
                                "quantity_sold": int(prod_qty)
                            }

        print()

    # Save JSON tree
    print("=" * 80)
    print("SAVING REVENUE ANALYSIS TREE")
    print("=" * 80)

    json_path = '/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/analysis_tree_total_revenue.json'
    with open(json_path, 'w') as f:
        json.dump(tree, f, indent=2)
    print(f"✓ JSON tree saved to: {json_path}")

    # Create CSV exports at each level
    print("\nCreating CSV exports...")

    # Revenue by Region
    region_csv = df.groupby('store_region').agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    region_csv.columns = ['region', 'revenue', 'transaction_count', 'unique_customers', 'total_quantity']
    region_csv['revenue_percentage'] = (region_csv['revenue'] / total_revenue * 100).round(2)
    region_csv['avg_transaction_value'] = (region_csv['revenue'] / region_csv['transaction_count']).round(2)
    region_csv = region_csv.sort_values('revenue', ascending=False)
    region_csv.to_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_region.csv', index=False)
    print("✓ revenue_by_region.csv")

    # Revenue by Store
    store_csv = df.groupby(['store_id', 'store_region', 'store_type']).agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    store_csv.columns = ['store_id', 'region', 'store_type', 'revenue', 'transaction_count', 'unique_customers', 'total_quantity']
    store_csv['revenue_percentage'] = (store_csv['revenue'] / total_revenue * 100).round(2)
    store_csv['avg_transaction_value'] = (store_csv['revenue'] / store_csv['transaction_count']).round(2)
    store_csv = store_csv.sort_values('revenue', ascending=False)
    store_csv.to_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_store.csv', index=False)
    print("✓ revenue_by_store.csv")

    # Revenue by Category
    category_csv = df.groupby('category').agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    category_csv.columns = ['category', 'revenue', 'transaction_count', 'unique_customers', 'total_quantity']
    category_csv['revenue_percentage'] = (category_csv['revenue'] / total_revenue * 100).round(2)
    category_csv['avg_transaction_value'] = (category_csv['revenue'] / category_csv['transaction_count']).round(2)
    category_csv = category_csv.sort_values('revenue', ascending=False)
    category_csv.to_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_category.csv', index=False)
    print("✓ revenue_by_category.csv")

    # Revenue by Sub-Category
    subcat_csv = df.groupby(['category', 'sub_category']).agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    subcat_csv.columns = ['category', 'sub_category', 'revenue', 'transaction_count', 'unique_customers', 'total_quantity']
    subcat_csv['revenue_percentage'] = (subcat_csv['revenue'] / total_revenue * 100).round(2)
    subcat_csv['avg_transaction_value'] = (subcat_csv['revenue'] / subcat_csv['transaction_count']).round(2)
    subcat_csv = subcat_csv.sort_values('revenue', ascending=False)
    subcat_csv.to_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_subcategory.csv', index=False)
    print("✓ revenue_by_subcategory.csv")

    # Revenue by Brand
    brand_csv = df.groupby(['category', 'brand']).agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    brand_csv.columns = ['category', 'brand', 'revenue', 'transaction_count', 'unique_customers', 'total_quantity']
    brand_csv['revenue_percentage'] = (brand_csv['revenue'] / total_revenue * 100).round(2)
    brand_csv['avg_transaction_value'] = (brand_csv['revenue'] / brand_csv['transaction_count']).round(2)
    brand_csv = brand_csv.sort_values('revenue', ascending=False)
    brand_csv.to_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_brand.csv', index=False)
    print("✓ revenue_by_brand.csv")

    # Revenue by SKU/Product
    sku_csv = df.groupby(['product_id', 'product_name', 'category', 'sub_category', 'brand']).agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    sku_csv.columns = ['product_id', 'product_name', 'category', 'sub_category', 'brand', 'revenue', 'transaction_count', 'unique_customers', 'total_quantity']
    sku_csv['revenue_percentage'] = (sku_csv['revenue'] / total_revenue * 100).round(2)
    sku_csv['avg_transaction_value'] = (sku_csv['revenue'] / sku_csv['transaction_count']).round(2)
    sku_csv = sku_csv.sort_values('revenue', ascending=False)
    sku_csv.to_csv('/Users/arghya.mukherjee/Downloads/cursor/sd ceo/claude/metadata_ceo/revenue_by_sku.csv', index=False)
    print("✓ revenue_by_sku.csv")

    print()
    print("=" * 80)
    print("✅ REVENUE ANALYSIS TREE COMPLETE!")
    print("=" * 80)
    print(f"Total Revenue Validated: ${total_revenue:,.2f}")
    print(f"Hierarchy Levels: 6 (Total → Region → Store → Category → Sub-Category → Brand → SKU)")
    print(f"Files Created: 7 (1 JSON + 6 CSVs)")

    return tree

if __name__ == "__main__":
    tree = build_revenue_tree()
