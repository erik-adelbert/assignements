#!/bin/sh

# This script automates the process of running unit tests and 
# measuring code coverage. It serves as a testing container
# entrypoint.

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
