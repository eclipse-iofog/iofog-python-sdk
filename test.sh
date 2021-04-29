#!/usr/bin/env bash

PYTHON_VERSION=$1

docker run --name send --network host -d iofog/test-python-sdk-send:$PYTHON_VERSION 1>/dev/null
docker run --name recieve --network host -d iofog/test-python-sdk-recieve:$PYTHON_VERSION 1>/dev/null

echo 'wait for 5 secs to check result....'
sleep 5s

SEND_CONTAINER_ID=$(docker ps -aqf "name=send")
RECIEVE_CONTAINER_ID=$(docker ps -aqf "name=recieve")

if [[ -z $RECIEVE_CONTAINER_ID || -z $SEND_CONTAINER_ID ]]; then
    echo 'Failed: either send container or recieve container is dead, please check'
    exit 1
fi

docker rm -f send 1>/dev/null
docker rm -f recieve 1>/dev/null


echo 'Success! '
exit 0
