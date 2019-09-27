#!/usr/bin/env python

# Copyright 2019, Alef Delpino, Delpinos
# All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted providing that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#  STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#  IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from os import chdir
from os.path import abspath, join, split

from setuptools import setup, find_packages

# Make sure we are standing in the correct directory.
# Old versions of distutils didn't take care of this.
here = split(abspath(__file__))[0]
chdir(here)


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


# Package metadata.
metadata = dict(
    name='dataproc',
    version='0.0.1.1',
    description='Data Processing and Transformation',
    author='Alef Bruno Delpino',
    author_email='alefdelpino@gmail.com',
    url='https://github.com/Delpinos/dataproc',
    license='GPL License',
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords='dataproc proc data etl tramsform process pipeline executor',
    packages=find_packages(),
    install_requires=['cryptography', 'pymongo']
)

# Get the long description from the readme file.
try:
    metadata['long_description'] = open(join(here, 'README.md'), 'rU').read()
except Exception:
    pass

setup(**metadata)
