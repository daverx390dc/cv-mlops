from aws_cdk import App
from infra.cdk.stack import MLOpsStack

app = App()
MLOpsStack(app, "cv-mlops-stack", env={
    "account": "123456789012",
    "region": "us-east-1"
})
app.synth()