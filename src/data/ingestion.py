import os
import boto3

def ingest_local_to_s3(local_dir, bucket, prefix):
    s3 = boto3.client('s3')
    for root, _, files in os.walk(local_dir):
        for f in files:
            path = os.path.join(root, f)
            key = os.path.join(prefix, os.path.relpath(path, local_dir))
            s3.upload_file(path, bucket, key)
            print(f"Uploaded {path} to s3://{bucket}/{key}")

if __name__ == "__main__":
    ingest_local_to_s3('data/raw', os.environ['RAW_BUCKET'], 'raw')