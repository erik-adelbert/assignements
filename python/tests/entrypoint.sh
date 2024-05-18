#!/bin/sh

TEST_PATH=$1

echo
echo "Performing unit tests:"
python -m pytest -v "${TEST_PATH}"

echo
echo "Measuring coverage:"
python -m coverage run -m pytest "${TEST_PATH}"

echo
echo "Coverage:"
python -m coverage report --show-missing
