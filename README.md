# MLOps Project — US Sales Prediction (End-to-End Pipeline)

**Author:** Ashutosh Somkuwar  
**Technologies:** Python, Scikit-Learn, DVC, MLflow, Prefect, FastAPI, Docker, GitHub Actions, Evidently AI

---

## 1. 📌 Project Overview

This project implements a complete **end-to-end MLOps pipeline** for predicting **Total Sales** from a US Sales dataset.

The pipeline includes:

- Data Preprocessing
- Exploratory Data Analysis (EDA)
- Model Training + Hyperparameters
- MLflow Experiment Tracking
- DVC Pipeline for reproducibility
- Prefect Workflow Orchestration
- FastAPI Model Deployment
- Docker Containerization
- GitHub Actions CI/CD
- Data Drift Monitoring using Evidently

This README describes how to **run the entire project step-by-step**.

---

## 2. 🗂 Project Structure

```
.
├── data/
│   ├── raw/
│   │   └── US_Sales_Datasets.csv
│   ├── processed/
│   └── eda/
│
├── notebooks/
│   ├── eda.ipynb
│   └── modeling_experiments.ipynb
│
├── src/
│   ├── api/app.py
│   ├── data/preprocess.py
│   ├── models/train.py
│   ├── models/evaluate.py
│   ├── models/predict.py
│   ├── flows/prefect_flow.py
│   └── monitoring/evidently_report.py
│
├── models/
│   └── model.pkl
│
├── reports/
│   └── evidently_report.html
│
├── dvc.yaml
├── params.yaml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
└── README.md
```

---

## 3. 📊 Dataset Description

The dataset contains:

- Retailer
- Retailer ID
- Invoice Date
- Region
- State
- City
- Product
- Price per Unit
- Units Sold
- Total Sales
- Operating Margin
- Operating Profit
- Sales Method

🎯 **Prediction Target:** Total Sales

---

## 4. 🔍 Exploratory Data Analysis (EDA)

Open the notebook:

```
jupyter notebook notebooks/eda.ipynb
```

EDA Includes:

- Missing Values
- Outlier Analysis
- Correlation Heatmap
- Sales Distribution
- Trend Analysis by Month/Year
- Region/State/Product Insights

Outputs saved to:

`data/eda/`

---

## 5. 🧹 Data Preprocessing

Run preprocessing:

```
python src/data/preprocess.py --input data/raw/US_Sales_Datasets.csv --output data/processed/sales_processed.csv
```

Preprocessing Tasks:

- Clean currency values
- Convert string → numeric
- Parse invoice date
- Add derived feature `Total_Sales_calc`
- Handle missing values

---

## 6. 📦 DVC Pipeline Setup

Initialize DVC:
```
dvc init
```

Run DVC pipeline:
```
dvc repro
```

Tracks:
- Raw → Processed Data
- Model Training
- Metrics
- Artifacts

---

## 7. 🤖 Model Training + MLflow Tracking

Train the model:
```
python src/models/train.py --data data/processed/sales_processed.csv --output models/model.pkl
```

Start MLflow UI:
```
mlflow ui --port 5000
```

Open UI: http://127.0.0.1:5000

Tracks:
- Parameters
- Metrics
- Models
- Evaluation Plots

---

## 8. 🧮 Model Evaluation

```
python src/models/evaluate.py
```

Outputs:
- RMSE
- MAE
- R² Score

---

## 9. ⚙️ Prefect Workflow Orchestration

Start Prefect:
```
prefect server start
```

Run the flow:
```
python src/flows/prefect_flow.py
```

UI: http://127.0.0.1:4200

---

## 10. 🌐 FastAPI Deployment

Run server:
```
uvicorn src.api.app:app --reload --port 8080
```

API Docs: http://127.0.0.1:8080/docs

Sample Input:
```json
{
  "Retailer_ID": 1185732,
  "Price_per_Unit": 45,
  "Units_Sold": 120,
  "Operating_Profit": 300,
  "Operating_Margin": 20,
  "Invoice_Year": 2023,
  "Invoice_Month": 10,
  "Total_Sales_calc": 5400
}
```

---

## 11. 🐳 Docker Containerization

Build image:
```
docker build -t sales-api .
```

Run container:
```
docker run -p 8080:8080 sales-api
```

---

## 12. 🔁 GitHub Actions CI/CD Pipeline

Workflow file: `.github/workflows/ci.yml`

Includes:
- flake8 linting
- Tests
- DVC validation
- Docker Build
- API healthcheck

Run locally:
```
flake8 src
```

---

## 13. 📈 Monitoring with Evidently AI

Run drift report:
```
python src/monitoring/evidently_report.py
```

Output saved to:
`reports/evidently_report.html`

---

## 14. 🚀 How to Run Entire Project (End-to-End)

```
pip install -r requirements.txt
python src/data/preprocess.py --input data/raw/US_Sales_Datasets.csv --output data/processed/sales_processed.csv
python src/models/train.py --data data/processed/sales_processed.csv --output models/model.pkl
python src/models/evaluate.py
mlflow ui --port 5000
dvc repro
prefect server start
python src/flows/prefect_flow.py
uvicorn src.api.app:app --reload --port 8080
docker build -t sales-api .
docker run -p 8080:8080 sales-api
python src/monitoring/evidently_report.py
```

---

## 15. 🏁 Final Notes

- Follows best DevOps & MLOps practices
- CI/CD ensures code quality
- MLflow + DVC ensure reproducibility
- Prefect automates workflows
- Docker enables deployment
- Evidently provides monitoring

---