#!/bin/sh

TEST_PATH=$1

python -m pytest -v "${TEST_PATH}"
python -m coverage run -m pytest "${TEST_PATH}"
python -m coverage report --show-missing
