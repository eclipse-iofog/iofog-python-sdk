#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

class IoFogException(Exception):
    def __init__(self, *args, **kwargs):
        super(IoFogException, self).__init__(*args, **kwargs)


class IoFogHttpException(IoFogException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'Error code: {}, reason: {}'.format(self.code, self.message)






