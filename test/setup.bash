#!/bin/bash

set -e

# Get variables
. test/conf/vars.bash

# Create namespace
iofogctl create namespace "$NS" -v
iofogctl configure current-namespace "$NS" -v

# Deploy local ECN
iofogctl deploy -f test/conf/ecn.yaml -v
