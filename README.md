# CV MLOps Pipeline

Production-ready pipeline for computer vision on AWS.

## Features
- Data versioning with DVC & S3
- Processing & training via SageMaker
- Dockerized inference endpoint
- CI/CD with GitHub Actions
- Monitoring & drift detection

## Quickstart
```bash
# Install deps
pip install -r requirements.txt

# Terraform deploy
cd infra/terraform/environments/dev
terraform init && terraform apply -auto-approve

# Run pipeline
python src/pipelines/pipeline.py