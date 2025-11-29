from prefect import flow, task
import subprocess

@task
def preprocessing():
    subprocess.run([
        "python", "src/data/preprocess.py",
        "data/raw/US_Sales_Datasets.csv",
        "data/processed/sales_processed.csv"
    ], check=True)

@task
def training():
    subprocess.run([
        "python", "src/models/train.py",
        "--data", "data/processed/sales_processed.csv",
        "--output", "models/model.pkl"
    ], check=True)

@flow
def mlops_pipeline():
    preprocessing()
    training()

if __name__ == "__main__":
    mlops_pipeline()
