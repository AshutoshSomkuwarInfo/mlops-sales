import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from lightgbm import LGBMRegressor
import joblib
import mlflow
import mlflow.sklearn

def prepare(df):
    df = df.select_dtypes(include=["number"]).copy()
    y = df.pop("Total Sales")
    return df, y

def train_model(data, output):
    df = pd.read_csv(data)
    X, y = prepare(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    mlflow.set_experiment("sales_mlops")

    with mlflow.start_run():
        model = LGBMRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1
        )
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        rmse = mean_squared_error(y_test, preds, squared=False)
        r2 = r2_score(y_test, preds)

        mlflow.log_metrics({"rmse": rmse, "r2": r2})
        mlflow.sklearn.log_model(model, "model")

        joblib.dump(model, output)
        print(f"Model saved → {output}")
        print(f"RMSE={rmse}, R2={r2}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    train_model(args.data, args.output)
