#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
from setuptools import setup, find_packages, Command

import binary_database_files

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
DESCRIPTION = (
    'A storage system for Django that stores uploaded files in both the '
    'database and file system.'
)


def get_reqs(*fns):
    lst = []
    for fn in fns:
        for package in open(os.path.join(CURRENT_DIR, fn)).readlines():
            package = package.strip()
            if not package:
                continue
            lst.append(package.strip())
    return lst

try:
    with io.open(os.path.join(CURRENT_DIR, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name='django-binary-database-files',
    version=binary_database_files.__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Roger Hunwicks',
    author_email='roger@tonic-solutions.com',
    url='https://github.com/kimetrica/django-binary-database-files/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 6 - Mature',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=get_reqs(
        'pip-requirements-min-django.txt',
        'pip-requirements.txt'
    ),
    tests_require=get_reqs('pip-requirements-test.txt'),
)
