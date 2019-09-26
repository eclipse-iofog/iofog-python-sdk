#!/usr/bin/env bash

PYTHON_VERSION=$1
if [[ ${PYTHON_VERSION} == "python3" ]]; then
  PYTHON_TAG="3.7-stretch"
else
  PYTHON_TAG="2.7-stretch"
fi

echo "Works"