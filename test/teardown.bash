#!/bin/bash

# Get variables
. test/conf/vars.bash

# Create namespace
iofogctl delete namespace "$NS" --force -v
