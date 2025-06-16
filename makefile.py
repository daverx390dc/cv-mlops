import os

structure = [
    'README.md',
    'LICENSE',
    '.gitignore',
    '.github/workflows/ci-cd.yaml',
    'infra/terraform/modules/networking/main.tf',
    'infra/terraform/modules/networking/variables.tf',
    'infra/terraform/modules/storage/main.tf',
    'infra/terraform/modules/storage/variables.tf',
    'infra/terraform/modules/compute/main.tf',
    'infra/terraform/modules/compute/variables.tf',
    'infra/terraform/modules/mlops/main.tf',
    'infra/terraform/modules/mlops/variables.tf',
    'infra/terraform/environments/dev/main.tf',
    'infra/terraform/environments/prod/main.tf',
    'infra/cdk/app.py',
    'src/data/ingestion.py',
    'src/data/processing.py',
    'src/features/featurization.py',
    'src/models/train.py',
    'src/models/inference.py',
    'src/pipelines/pipeline.py',
    'src/utils/logger.py',
    'src/config.yaml',
    'tests/unit/test_train.py',
    'tests/integration/test_pipeline.py',
    'notebooks/exploration.ipynb',
    'Dockerfile',
    'requirements.txt',
    'setup.py',
]

for path in structure:
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    open(path, 'a').close()