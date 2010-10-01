#!/usr/bin/env python

# FIXME add boto dependency, or split the package in different projects, the core and the APIs

from distutils.core import setup

setup(
    name='cloud-tool',
    version='0.0.1',
    description='Command-line tool to manage computing clouds',
    author='Manuel Amador',
    author_email='rudd-o@rudd-o.com',
    url='http://github.com/Rudd-O/cloud-tool',
    packages=['cloudtool','cloudtool.apis'],
    scripts=['bin/cloud-tool'],
)