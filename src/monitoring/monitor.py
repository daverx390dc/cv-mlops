import os
import boto3
import pandas as pd
from io import StringIO
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def generate_drift_report(
    reference_dataset_s3_uri: str,
    production_dataset_s3_uri: str,
    report_bucket: str,
    report_prefix: str = 'evidently-reports/'
):
    s3 = boto3.client('s3')

    def read_s3_csv(uri: str) -> pd.DataFrame:
        bucket, key = uri.replace('s3://', '').split('/', 1)
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))

    # Load reference and production data
    ref_data = read_s3_csv(reference_dataset_s3_uri)
    prod_data = read_s3_csv(production_dataset_s3_uri)

    # Initialize an Evidently report for data drift
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_data, current_data=prod_data)

    # Generate output
    result_json = report.as_json()
    result_html = report.as_html()

    # Upload reports to S3
    json_key = f"{report_prefix}drift_report.json"
    html_key = f"{report_prefix}drift_report.html"
    s3.put_object(Bucket=report_bucket, Key=json_key, Body=result_json)
    s3.put_object(Bucket=report_bucket, Key=html_key, Body=result_html)
    print(f"Evidently drift report uploaded to s3://{report_bucket}/{report_prefix}")
