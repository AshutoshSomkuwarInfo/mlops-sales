import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

train = pd.read_csv("data/processed/sales_processed.csv").head(500)
current = pd.read_csv("data/processed/sales_processed.csv").tail(500)

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=train, current_data=current)
report.save_html("reports/evidently_report.html")

print("Evidently report saved → reports/evidently_report.html")
