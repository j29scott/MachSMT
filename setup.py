#!/usr/bin/env python3

import os

from setuptools import setup, find_packages

setup(
    name         = 'machsmt',
    version      = '0.1',
    description  = 'An algorithm selection tool for SMT-LIB solvers',
    author       = 'Joe Scott, Aina Niemetz, Mathias Preiner, Vijay Ganesh',
    author_email = 'joseph.scott@uwaterloo.ca',
    url          = 'https://github.com/j29scott/smtzilla',
    scripts      = [
        'bin/machsmt_build',
        'bin/machsmt_select',
    ],
    packages     = find_packages(),
    package_dir  = {
        'machsmt': 'machsmt',
    },
)