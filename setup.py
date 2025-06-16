from setuptools import setup, find_packages

setup(
    name='cv_mlops',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    install_requires=[
        'boto3','opencv-python-headless','torch','torchvision',
        'fastapi','uvicorn','sagemaker','dvc','mlflow'
    ],
    entry_points={
        'console_scripts':[
            'run-pipeline=src.pipelines.pipeline:main'
        ]
    }
)