#!/usr/bin/env bash

PYTHON_VERSIONS=( "python3" "python2" )
FAILURES=( 0 0 )

idx=0
for version in ${PYTHON_VERSIONS[@]}; do

    docker run --name send -d iofog/test-python-sdk-send:$version 1>/dev/null
    docker run --name recieve -d iofog/test-python-sdk-recieve:$version 1>/dev/null

    SEND_CONTAINER_ID=$(docker ps -aqf "name=send")
    RECIEVE_CONTAINER_ID=$(docker ps -aqf "name=recieve")

    if [[ -z $RECIEVE_CONTAINER_ID || -z $SEND_CONTAINER_ID ]]; then
        echo "${version} has failed to send/recieve data"
        ${FAILURES[idx]} = 1
    fi
    idx+=1

    docker rm -f send 1>/dev/null
    docker rm -f recieve 1>/dev/null
done

for failure in ${FAILURES[@]}; do
    if [[ ${failure} == 1 ]]; then
        exit 1
    fi
done

exit 0
