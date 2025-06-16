import os
from sagemaker import get_execution_role
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CreateModelStep
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.tensorflow import TensorFlow
from sagemaker.workflow.parameters import ParameterString, ParameterInteger
from sagemaker.inputs import TrainingInput
from sagemaker.model_metrics import MetricsSource, ModelMetrics
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.functions import Join
from sagemaker.workflow.cache_config import CacheConfig

# Pipeline parameters
instance_type = ParameterString(name="InstanceType", default_value="ml.m5.large")
instance_count = ParameterInteger(name="InstanceCount", default_value=1)
processing_instance_count = ParameterInteger(name="ProcessingInstanceCount", default_value=1)

# Execution role
role = get_execution_role()

# S3 bucket names (from environment)
raw_bucket = os.environ['RAW_BUCKET']
processed_bucket = os.environ['PROCESSED_BUCKET']
model_bucket = os.environ['MODEL_BUCKET']

# URIs
processing_input_uri = f"s3://{raw_bucket}/raw/"
processing_output_uri = f"s3://{processed_bucket}/processed/"
model_artifact_prefix = "sagemaker/cv-models"

# 1. Data Preprocessing Step
processor = SKLearnProcessor(
    framework_version="0.23-1",
    role=role,
    instance_type=instance_type,
    instance_count=processing_instance_count,
    base_job_name="cv-preprocess"
)
processing_step = ProcessingStep(
    name="DataPreprocessing",
    processor=processor,
    inputs=[ProcessingInput(source=processing_input_uri, destination="/opt/ml/processing/input")],
    outputs=[ProcessingOutput(source="/opt/ml/processing/output", destination=processing_output_uri, output_name="processed")],
    code="src/data/processing.py",
    cache_config=CacheConfig(enable_caching=True, expire_after="24h")
)

# 2. Model Training Step
estimator = TensorFlow(
    entry_point="src/models/train.py",
    role=role,
    instance_count=instance_count,
    instance_type=instance_type,
    framework_version="2.4",
    py_version="py37",
    output_path=f"s3://{model_bucket}/{model_artifact_prefix}"
)
training_step = TrainingStep(
    name="ModelTraining",
    estimator=estimator,
    inputs={
        "training": TrainingInput(
            s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["processed"].S3Output.S3Uri,
            content_type="application/x-image"
        )
    }
)

# 3. Model Registration Step
evaluation_report = PropertyFile(
    name="EvaluationReport",
    output_name="evaluation",
    path="evaluation.json"
)
model_metrics = ModelMetrics(
    model_statistics=MetricsSource(
        s3_uri=Join(on="/", values=[
            training_step.properties.ModelArtifacts.S3ModelArtifacts,
            "evaluation.json"
        ]),
        content_type="application/json"
    )
)
model = estimator.create_model(role=role, model_server_workers=1)
create_model_step = CreateModelStep(
    name="RegisterModel",
    model=model,
    model_metrics=model_metrics
)

# 4. Assemble Pipeline
pipeline = Pipeline(
    name="CVMLOpsPipeline",
    parameters=[instance_type, instance_count, processing_instance_count],
    steps=[processing_step, training_step, create_model_step]
)

if __name__ == "__main__":
    pipeline.upsert(role_arn=role)
    print("SageMaker pipeline created/updated")
