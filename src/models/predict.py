import joblib
import pandas as pd


def load_model(path="models/model.pkl"):
    return joblib.load(path)


def predict(data: dict):
    df = pd.DataFrame([data])
    model = load_model()
    pred = model.predict(df)[0]
    return float(pred)
