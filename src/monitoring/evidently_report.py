import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

df = pd.read_csv("data/processed/sales_processed.csv")
train = df.head(500)
current = df.tail(500)

# Keep only columns that have at least 1 non-null value
valid_columns = train.columns[train.notna().any()]
train = train[valid_columns]
current = current[valid_columns]

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=train, current_data=current)
report.save_html("reports/evidently_report.html")
print("Saved evidently_report.html")
