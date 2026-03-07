import pandas as pd

import sys

try:
    # First try reading it as an excel file given the .xlsx extension
    df = pd.read_excel('all_data.csv.xlsx', engine='openpyxl')
except Exception as e:
    print(f"Failed to read as excel, trying CSV: {e}")
    # Try reading as csv if that fails
    df = pd.read_csv('all_data.csv.xlsx')

# Initial row count
print(f"Initial rows: {len(df)}")

# Drop rows where any column has NA/NaN
df_clean = df.dropna()
print(f"Rows after dropping NA: {len(df_clean)}")

# Get top 1000
df_final = df_clean.head(1000)
print(f"Final rows selected: {len(df_final)}")

# Save to new Excel file
df_final.to_excel('filtered_data.xlsx', index=False)
print("Data successfully saved to filtered_data.xlsx!")
