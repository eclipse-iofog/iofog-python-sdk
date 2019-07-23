#!/usr/bin/env bash

PYTHON_VERSION=$1
if [[ ${PYTHON_VERSION} == "python3" ]]; then
  PYTHON_TAG="3.7-stretch"
else
  PYTHON_TAG="2.7-stretch"
fi

# Build Python Images
docker build --build-arg TAG_NAME=${PYTHON_TAG} -t iofog/test-python-sdk-send:${PYTHON_VERSION} -f ./Docker/Dockerfile.send .
docker build --build-arg TAG_NAME=${PYTHON_TAG} -t iofog/test-python-sdk-recieve:${PYTHON_VERSION} -f ./Docker/Dockerfile.recieve .

# Push Python Images
docker push iofog/test-python-sdk-send:${PYTHON_VERSION}
docker push iofog/test-python-sdk-recieve:${PYTHON_VERSION}