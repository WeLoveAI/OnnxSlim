import argparse
import glob
import os
import subprocess

import pytest


def parse_arguments():
    parser = argparse.ArgumentParser(description="Test script for ONNX models")
    parser.add_argument(
        "--model-dir",
        type=str,
        required=True,
        help="Directory containing ONNX model files",
    )
    return parser.parse_args()


args = parse_arguments()


@pytest.fixture(params=glob.glob(f"{args.model_dir}/*/*.onnx"))
def model_file(request):
    yield request.param


def test_model_file(model_file):
    slim_model_file = model_file.replace(".onnx", "_slim.onnx")
    command = f"onnxslim {model_file} {slim_model_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        raise AssertionError("Failed to slim model")
    else:
        output = result.stdout
        print(f"\n{output}")
        os.remove(slim_model_file)
        slim_data_file = model_file.replace(".onnx", "_slim.onnx.data")
        if os.path.exists(slim_data_file):
            os.remove(slim_data_file)


if __name__ == "__main__":
    pytest.main(
        [
            "-p",
            "no:warnings",
            "-sv",
            "tests/test_folder.py",
        ]
    )
