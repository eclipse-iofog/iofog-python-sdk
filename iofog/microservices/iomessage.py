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

from struct import pack, unpack
import sys

from iofog.microservices.util import *
import base64

from iofog.microservices.definitions import *


# todo check fields == None?
class IoMessage:
    def __init__(self):
        self.id = ''
        self.tag = ''
        self.groupid = ''
        self.version = IO_MESSAGE_VERSION
        self.sequencenumber = 0
        self.sequencetotal = 0
        self.priority = 0
        self.timestamp = 0
        self.publisher = ''
        self.authid = ''
        self.authgroup = ''
        self.chainposition = 0
        self.hash = ''
        self.previoushash = ''
        self.nonce = ''
        self.difficultytarget = 0
        self.infotype = ''
        self.infoformat = ''
        self.contextdata = bytearray()
        self.contentdata = bytearray()

    def to_bytearray(self):
        if self.version != IO_MESSAGE_VERSION:
            raise Exception('Incompatible IoMessage version')

        header = bytearray()
        body = bytearray()
        # version
        header.extend(pack('>H', self.version))
        # id
        header.extend(pack('>B', len(self.id)))
        body.extend(self.id.encode())
        # tag
        header.extend(pack('>H', len(self.tag)))
        body.extend(self.tag.encode())
        # group id
        header.extend(pack('>B', len(self.groupid)))
        body.extend(self.groupid.encode())
        # sequence number
        byte_num, byte_num_len = num_to_bytearray(self.sequencenumber)
        header.extend(pack('>B', byte_num_len))
        body.extend(byte_num)
        # sequence total
        byte_num, byte_num_len = num_to_bytearray(self.sequencetotal)
        header.extend(pack('>B', byte_num_len))
        body.extend(byte_num)
        # priority
        byte_num, byte_num_len = num_to_bytearray(self.priority)
        header.extend(pack('>B', byte_num_len))
        body.extend(byte_num)
        # timestamp
        byte_num, byte_num_len = num_to_bytearray(self.timestamp)
        header.extend(pack('>B', byte_num_len))
        body.extend(byte_num)
        # publisher
        header.extend(pack('>B', len(self.publisher)))
        body.extend(self.publisher.encode())
        # auth id
        header.extend(pack('>H', len(self.authid)))
        body.extend(self.authid.encode())
        # auth group
        header.extend(pack('>H', len(self.authgroup)))
        body.extend(self.authgroup.encode())
        # chain position
        byte_num, byte_num_len = num_to_bytearray(self.chainposition)
        header.extend(pack('>B', byte_num_len))
        body.extend(byte_num)
        # hash
        header.extend(pack('>H', len(self.hash)))
        body.extend(self.hash.encode())
        # previous hash
        header.extend(pack('>H', len(self.previoushash)))
        body.extend(self.previoushash.encode())
        # nonce
        header.extend(pack('>H', len(self.nonce)))
        body.extend(self.nonce.encode())
        # difficulty target
        byte_num, byte_num_len = num_to_bytearray(self.difficultytarget)
        header.extend(pack('>B', byte_num_len))
        body.extend(byte_num)
        # info type
        header.extend(pack('>B', len(self.infotype)))
        body.extend(self.infotype.encode())
        # info format
        header.extend(pack('>B', len(self.infoformat)))
        body.extend(self.infoformat.encode())
        # context data
        header.extend(pack('>I', len(self.contextdata)))
        body.extend(self.contextdata.encode())
        # content data
        header.extend(pack('>I', len(self.contentdata)))
        body.extend(self.contentdata.encode())

        return header + body

    @staticmethod
    def from_bytearray(bytes):
        msg = IoMessage()
        msg.version = unpack('>H', bytes[:2])[0]
        if msg.version != IO_MESSAGE_VERSION:
            raise Exception('Incompatible IoMessage version')

        data_offset = 33
        # id
        field_len = bytes[2]
        msg.id = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # tag
        field_len = unpack('>H', bytes[3:5])[0]
        msg.tag = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # group id
        field_len = bytes[5]
        msg.groupid = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # sequence number
        field_len = bytes[6]
        msg.sequencenumber = bytearray_to_num(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # sequence total
        field_len = bytes[7]
        msg.sequencetotal = bytearray_to_num(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # priority
        field_len = bytes[8]
        msg.priority = bytearray_to_num(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # timestamp
        field_len = bytes[9]
        msg.timestamp = bytearray_to_num(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # publisher
        field_len = bytes[10]
        msg.publisher = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # auth id
        field_len = unpack('>H', bytes[11:13])[0]
        msg.authid = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # auth group
        field_len = unpack('>H', bytes[13:15])[0]
        msg.authgroup = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # chain position
        field_len = bytes[15]
        msg.chainposition = bytearray_to_num(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # hash
        field_len = unpack('>H', bytes[16:18])[0]
        msg.hash = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # previous hash
        field_len = unpack('>H', bytes[18:20])[0]
        msg.previoushash = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # nonce
        field_len = unpack('>H', bytes[20:22])[0]
        msg.nonce = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # difficulty target
        field_len = bytes[22]
        msg.difficultytarget = bytearray_to_num(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # info type
        field_len = bytes[23]
        msg.infotype = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # info format
        field_len = bytes[24]
        msg.infoformat = str(bytes[data_offset: data_offset + field_len])
        data_offset += field_len
        # context data
        field_len = unpack('>I', bytes[25:29])[0]
        msg.contextdata = bytes[data_offset: data_offset + field_len]
        data_offset += field_len
        # content data
        field_len = unpack('>I', bytes[29:33])[0]
        msg.contentdata = bytes[data_offset: data_offset + field_len]
        return msg

    @staticmethod
    def from_json(json_msg):
        if isinstance(json_msg, str):
            json_msg = json.loads(json_msg)
        msg = IoMessage()
        msg.id = json_msg.get(ID, '')
        msg.tag = json_msg.get(TAG, '')
        msg.groupid = json_msg.get(GROUP_ID, '')
        msg.version = json_msg.get(VERSION, 0)
        msg.timestamp = json_msg.get(TIMESTAMP, 0)
        msg.sequencenumber = json_msg.get(SEQUENCE_NUMBER, 0)
        msg.sequencetotal = json_msg.get(SEQUENCE_TOTAL, 0)
        msg.priority = json_msg.get(PRIORITY, 0)
        msg.publisher = json_msg.get(PUBLISHER, '')
        msg.authid = json_msg.get(AUTH_ID, '')
        msg.authgroup = json_msg.get(AUTH_GROUP, '')
        msg.chainposition = json_msg.get(CHAIN_POSITION, 0)
        msg.hash = json_msg.get(HASH, '')
        msg.previoushash = json_msg.get(PREVIOUS_HASH, '')
        msg.nonce = json_msg.get(NONCE, '')
        msg.difficultytarget = json_msg.get(DIFFICULTY_TARGET, 0)
        msg.infotype = json_msg.get(INFO_TYPE, '')
        msg.infoformat = json_msg.get(INFO_FORMAT, '')
        contextdata = json_msg.get(CONTEXT_DATA, '')
        contextdata = base64.b64decode(contextdata)
        msg.contextdata = str.encode(contextdata)
        contentdata = json_msg.get(CONTENT_DATA, '')
        contentdata = base64.b64decode(contentdata)
        msg.contentdata = str.encode(contentdata)
        return msg

    def to_json(self):
        json_msg = {
            VERSION: self.version,
            ID: self.id,
            TAG: self.tag,
            GROUP_ID: self.groupid,
            TIMESTAMP: self.timestamp,
            SEQUENCE_NUMBER: self.sequencenumber,
            SEQUENCE_TOTAL: self.sequencetotal,
            PRIORITY: self.priority,
            PUBLISHER: self.publisher,
            AUTH_ID: self.authid,
            AUTH_GROUP: self.authgroup,
            CHAIN_POSITION: self.chainposition,
            HASH: self.hash,
            PREVIOUS_HASH: self.previoushash,
            NONCE: self.nonce,
            DIFFICULTY_TARGET: self.difficultytarget,
            INFO_TYPE: self.infotype,
            INFO_FORMAT: self.infoformat,
            CONTEXT_DATA: base64.b64encode(self.contextdata),
            CONTENT_DATA: base64.b64encode(self.contentdata)
        }
        return json.dumps(json_msg)
