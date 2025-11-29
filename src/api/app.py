from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# Load trained model
model = joblib.load("models/model.pkl")

# Pydantic model MUST match the training features exactly
class SalesInput(BaseModel):
    Retailer_ID: int
    Price_per_Unit: float
    Units_Sold: float
    Operating_Profit: float
    Operating_Margin: float
    Invoice_Year: int
    Invoice_Month: int
    Total_Sales_calc: float

@app.post("/predict")
def predict_sales(data: SalesInput):
    # Convert input to DataFrame
    df = pd.DataFrame([{
        "Retailer ID": data.Retailer_ID,
        "Price per Unit": data.Price_per_Unit,
        "Units Sold": data.Units_Sold,
        "Operating Profit": data.Operating_Profit,
        "Operating Margin": data.Operating_Margin,
        "Invoice_Year": data.Invoice_Year,
        "Invoice_Month": data.Invoice_Month,
        "Total_Sales_calc": data.Total_Sales_calc
    }])

    # Predict
    pred = model.predict(df)[0]
    return {"predicted_sales": float(pred)}
