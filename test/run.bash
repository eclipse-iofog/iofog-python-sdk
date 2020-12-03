#!/bin/bash

set -e

# Get test names from args, run all if empty
TESTS="$1"
if [ -z "$TESTS" ]; then
    TESTS=("rest")
fi

# Run specified tests
for TEST in ${TESTS[@]}; do
    pytest -v "test/${TEST}.py"
done
