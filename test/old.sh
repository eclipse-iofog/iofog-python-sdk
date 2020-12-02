#!/usr/bin/env bash

PYTHON_VERSION=$1

docker run --name send -d iofog/test-python-sdk-send:$PYTHON_VERSION 1>/dev/null
docker run --name recieve -d iofog/test-python-sdk-recieve:$PYTHON_VERSION 1>/dev/null

SEND_CONTAINER_ID=$(docker ps -aqf "name=send")
RECIEVE_CONTAINER_ID=$(docker ps -aqf "name=recieve")

if [[ -z $RECIEVE_CONTAINER_ID || -z $SEND_CONTAINER_ID ]]; then
    exit 1
fi

docker rm -f send 1>/dev/null
docker rm -f recieve 1>/dev/null

exit 0
