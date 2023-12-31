import glob
import subprocess

import pytest


@pytest.fixture(params=glob.glob("model/*.onnx"))
def model_file(request):
    yield request.param


def test_model_file(model_file):
    slim_model_file = model_file.replace(".onnx", "_slim.onnx")
    command = f"onnxslim {model_file} {slim_model_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stderr.strip()
    # Assert the expected return code
    print(output)
    assert result.returncode == 0
