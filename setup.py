#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

from distutils.core import setup

setup(
    name='iofog-python-sdk',
    version='1.0.0',
    project_urls={
        'Documentation': 'https://github.com/ioFog/iofog-python-sdk/blob/master/README.md',
        'Source': 'https://github.com/ioFog/iofog-python-sdk.git',
        'Tracker': 'https://github.com/ioFog/iofog-python-sdk/issues',
        'Eclipse ioFog': 'http://iofog.org'
    },
    packages=['iofog_python_sdk'],
    url='https://github.com/ioFog/iofog-python-sdk',
    license='EPL-2.0',
    author='Eclipse ioFog',
    author_email='edgemaster@iofog.org',
    description='Native python SDK for Eclipse ioFog development.',
    requires=['ws4py'],
    keywords='iofog IoT Eclipse fog computing edgeworx',
)
