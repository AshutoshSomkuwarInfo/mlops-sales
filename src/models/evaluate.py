# src/models/evaluate.py

import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, r2_score


def evaluate(model_path, data_path):
    model = joblib.load(model_path)
    df = pd.read_csv(data_path)

    X = df.select_dtypes(include=["number"]).drop("Total Sales", axis=1)
    y = df["Total Sales"]

    preds = model.predict(X)

    # ---- FIXED RMSE (no squared=False) ----
    mse = mean_squared_error(y, preds)
    rmse = mse ** 0.5
    # ---------------------------------------

    r2 = r2_score(y, preds)

    print("RMSE:", rmse)
    print("R2:", r2)

    return rmse, r2


if __name__ == "__main__":
    evaluate("models/model.pkl", "data/processed/sales_processed.csv")
