#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='iofog',
    version='3.0.0-beta1',
    project_urls={
        'Documentation': 'https://github.com/eclipse-iofog/iofog-python-sdk/blob/master/README.md',
        'Source': 'https://github.com/eclipse-iofog/iofog-python-sdk.git',
        'Tracker': 'https://github.com/eclipse-iofog/iofog-python-sdk/issues',
        'Eclipse ioFog': 'http://iofog.org'
    },
    packages=setuptools.find_packages(),
    url='https://github.com/eclipse-iofog/iofog-python-sdk',
    license='EPL-2.0',
    author='Eclipse ioFog',
    author_email='edgemaster@iofog.org',
    description='Python SDK for Eclipse ioFog development.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    requires=['ws4py', 'json', 'requests'],
    keywords='ioFog IoT Eclipse fog computing edgeworx',
)
