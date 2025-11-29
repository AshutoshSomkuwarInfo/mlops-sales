import pandas as pd
import numpy as np


def clean_num(x):
    if pd.isna(x):
        return np.nan

    s = str(x).replace(",", "").replace("$", "").strip()
    try:
        return float(s)
    except Exception:
        return np.nan


def preprocess(input_path, output_path):
    df = pd.read_csv(input_path)

    numeric_cols = [
        "Price per Unit",
        "Units Sold",
        "Total Sales",
        "Operating Profit",
        "Operating Margin",
    ]

    for col in numeric_cols:
        df[col] = df[col].apply(clean_num)

    df["Invoice Date"] = pd.to_datetime(df["Invoice Date"], errors="coerce")
    df["Invoice_Year"] = df["Invoice Date"].dt.year
    df["Invoice_Month"] = df["Invoice Date"].dt.month

    df["Total_Sales_calc"] = df["Price per Unit"] * df["Units Sold"]

    df.to_csv(output_path, index=False)
    print(f"Saved cleaned file: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    preprocess(args.input, args.output)
