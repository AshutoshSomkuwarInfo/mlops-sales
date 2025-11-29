import joblib
import pandas as pd

def predict(model_path, row: dict):
    model = joblib.load(model_path)
    df = pd.DataFrame([row])
    return model.predict(df)[0]
