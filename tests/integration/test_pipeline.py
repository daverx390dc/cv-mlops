import subprocess

def test_pipeline_execution():
    result = subprocess.run(['python','src/pipelines/pipeline.py'], capture_output=True)
    assert result.returncode == 0