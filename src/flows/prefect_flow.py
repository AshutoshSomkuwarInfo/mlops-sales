from prefect import flow, task
from src.data.preprocess import preprocess
from src.models.train import train_model


@task
def preprocess_task(input_path, output_path):
    preprocess(input_path, output_path)


@task
def train_task(data_path, model_path):
    train_model(data_path, model_path)


@flow
def main_flow():
    preprocess_task("data/raw/US_Sales_Datasets.csv",
                    "data/processed/sales_processed.csv")

    train_task("data/processed/sales_processed.csv",
               "models/model.pkl")


if __name__ == "__main__":
    main_flow()
