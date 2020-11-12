#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

import json
import math

try:
    import urllib.request as urllib_request #for python 3
except ImportError:
    import urllib2 as urllib_request # for python 2

from struct import pack
from iofog.microservices.definitions import CODE_MSG


def num_to_bytearray(num):
    if num == 0:
        return bytearray([0]), 1

    num_of_bits = num.bit_length()
    num_of_bytes = int(math.ceil(num_of_bits / 8.0))
    b = bytearray(num_of_bytes)
    shift = 8 * (num_of_bytes - 1)
    for i in range(num_of_bytes):
        b[i] = (num >> shift) & 0xFF
        shift -= 8
    return b, num_of_bytes


def bytearray_to_num(arr):
    num = 0
    shift = 0
    for i in reversed(arr):
        num += i << shift
        shift += 8
    return num


def make_post_request(url, body_type, body):
    req = urllib_request.Request(url, body, {'Content-Type': body_type})
    response = urllib_request.urlopen(req)
    return json.loads(response.read())

def make_get_request(url, body_type, body):
    req = urllib_request.Request(url, body, {'Content-Type': body_type}, method="GET")
    response = urllib_request.urlopen(req)
    return json.loads(response.read())


def prepare_iomessage_for_sending_via_socket(io_msg):
    msg_bytes = io_msg.to_bytearray()
    package = bytearray([CODE_MSG])
    package.extend(pack('>I', len(msg_bytes)))
    return package + msg_bytes
