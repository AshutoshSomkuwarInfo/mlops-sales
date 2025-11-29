# src/models/train.py

import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import mlflow
import mlflow.sklearn
from lightgbm import LGBMRegressor


def prepare(df):
    """Keep only numeric columns and separate features/target."""
    df = df.select_dtypes(include=["number"]).copy()
    y = df.pop("Total Sales")
    return df, y


def train_model(data, output):
    # Load data
    df = pd.read_csv(data)
    X, y = prepare(df)
    print("TRAINING FEATURES:", list(X.columns))

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # MLflow experiment
    mlflow.set_experiment("sales_mlops")

    with mlflow.start_run():
        model = LGBMRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            random_state=42
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        # ---- FIXED RMSE (no squared=False) ----
        mse = mean_squared_error(y_test, preds)
        rmse = mse ** 0.5
        # ---------------------------------------

        r2 = r2_score(y_test, preds)

        # Log params & metrics
        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 8)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        # Save model
        mlflow.sklearn.log_model(model, "model")
        joblib.dump(model, output)

        print(f"Model saved to: {output}")
        print(f"RMSE: {rmse}")
        print(f"R2: {r2}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    train_model(args.data, args.output)
