from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

model = joblib.load("models/model.pkl")

class SalesInput(BaseModel):
    Price_per_Unit: float
    Units_Sold: float
    Operating_Margin: float = 0
    Operating_Profit: float = 0
    Year: int = 2023
    Month: int = 1

@app.post("/predict")
def predict_sales(body: SalesInput):
    df = pd.DataFrame([body.dict()])
    pred = model.predict(df)[0]
    return {"predicted_sales": float(pred)}
