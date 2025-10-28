#!/usr/bin/env python3
"""
Convert grocery dataset from INR to USD
Exchange rate: 1 USD = 83 INR (as of 2025)
"""
import pandas as pd
import sys

# Configuration
INR_TO_USD = 83.0
INPUT_FILE = '/Users/arghya.mukherjee/Downloads/cursor/sd/grocery_dataset.csv'
OUTPUT_FILE = '/Users/arghya.mukherjee/Downloads/cursor/sd/grocery_dataset_usd.csv'

def convert_currency(value):
    """Convert INR to USD"""
    if pd.isna(value):
        return value
    return round(float(value) / INR_TO_USD, 2)

print(f"Starting conversion from INR to USD...")
print(f"Exchange rate: 1 USD = {INR_TO_USD} INR")
print(f"Reading dataset: {INPUT_FILE}")

# Read dataset in chunks to handle large file
chunk_size = 100000
chunks = []
total_rows = 0

# Process in chunks
for chunk in pd.read_csv(INPUT_FILE, chunksize=chunk_size):
    # Convert price columns from INR to USD
    chunk['unit_price'] = chunk['unit_price'].apply(convert_currency)
    chunk['final_price'] = chunk['final_price'].apply(convert_currency)
    chunk['total_amount'] = chunk['total_amount'].apply(convert_currency)

    chunks.append(chunk)
    total_rows += len(chunk)
    print(f"Processed {total_rows} rows...")

# Combine all chunks
print(f"Combining chunks...")
df = pd.concat(chunks, ignore_index=True)

# Save to new file
print(f"Saving to: {OUTPUT_FILE}")
df.to_csv(OUTPUT_FILE, index=False)

print(f"✓ Conversion complete!")
print(f"  Total rows processed: {total_rows:,}")
print(f"  Output file: {OUTPUT_FILE}")
print(f"  Sample conversions:")
print(f"    ₹83.00 → ${1.00}")
print(f"    ₹830.00 → ${10.00}")
print(f"    ₹8,300.00 → ${100.00}")
