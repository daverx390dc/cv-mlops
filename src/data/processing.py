import os
import cv2
import boto3
import numpy as np
from pathlib import Path

def preprocess_and_upload(bucket, input_prefix, output_prefix):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)

    for obj in bucket.objects.filter(Prefix=input_prefix):
        if not obj.key.lower().endswith(('.jpg','.png')): 
            continue
        data = obj.get()['Body'].read()
        img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        img = cv2.resize(img, (224,224))
        _, buf = cv2.imencode('.jpg', img)
        bucket.put_object(Key=obj.key.replace(input_prefix, output_prefix), Body=buf.tobytes())
        print(f"Processed {obj.key}")

if __name__ == "__main__":
    preprocess_and_upload(os.environ['PROCESSED_BUCKET'],'raw/','processed/')