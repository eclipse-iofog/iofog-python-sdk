#!/usr/bin/env bash

PYTHON_VERSIONS=( "python3" "python2" )
FAILURES=( 0 0 )

idx=0
for version in ${PYTHON_VERSIONS[@]}; do

    docker pull iofog/test-python-sdk-send::${version}
    docker pull iofog/test-python-sdk-recieve:${version}

    docker run -d iofog/test-python-sdk-send:${version}
    docker run -d iofog/test-python-sdk-recieve:${version}

    RECIEVE_CONTAINER_ID=$( docker ps | grep "python recieve.py" | awk '{print $1}' )
    SEND_CONTAINER_ID=$( docker ps | grep "python send.py" | awk '{print $1}' )

    if [[ "${RECIEVE_CONTAINER_ID}" -eq "" || "${SEND_CONTAINER_ID}" -eq "" ]]; then
        echo "${version} has failed to send/recieve data"
        ${FAILURES[idx]}= 1
    fi
    idx+=1
done

for failure in ${FAILURES[@]}; do
    if [[ ${failure} == 1 ]]; then
        exit 1
    fi
done

exit 0
