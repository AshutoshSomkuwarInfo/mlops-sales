# src/data/preprocess.py
import pandas as pd
import numpy as np
from pathlib import Path

def clean_currency(x):
    if pd.isna(x): return np.nan
    # remove commas, $ etc
    s = str(x).replace(',','').replace('$','').strip()
    try:
        return float(s)
    except:
        return np.nan

def load_raw(path):
    return pd.read_csv(path)

def preprocess(df: pd.DataFrame):
    df = df.copy()
    # parse date
    if 'Invoice Date' in df.columns:
        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')
        df['Invoice_Year'] = df['Invoice Date'].dt.year
        df['Invoice_Month'] = df['Invoice Date'].dt.month
    # numeric conversions
    for col in ['Total Sales','Operating Profit','Operating Margin','Units Sold','Price per Unit']:
        if col in df.columns:
            df[col] = df[col].apply(clean_currency)
    # Units Sold might be integer-like
    if 'Units Sold' in df.columns:
        df['Units Sold'] = pd.to_numeric(df['Units Sold'], errors='coerce')

    # Feature engineering: Price * Units (if missing Total Sales)
    if 'Total Sales' in df.columns and 'Price per Unit' in df.columns and 'Units Sold' in df.columns:
        df['Total_Sales_calc'] = df['Price per Unit'] * df['Units Sold']
        df['Total Sales'] = df['Total Sales'].fillna(df['Total_Sales_calc'])

    # drop rows with missing target
    df = df.dropna(subset=['Total Sales'])
    return df

def run(input_path, output_path):
    df = load_raw(input_path)
    dfp = preprocess(df)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    dfp.to_csv(output_path, index=False)
    print(f"Saved processed data to {output_path}")

if __name__=='__main__':
    import sys
    run(sys.argv[1], sys.argv[2])
