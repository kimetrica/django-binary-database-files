#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import database_files
setup(
    name='django-database-files',
    version=database_files.__version__,
    description='A storage system for Django that stores uploaded files in both the database and file system.',
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='http://github.com/chrisspen/django-database-files',
    packages=[
        'database_files',
        'database_files.management',
        'database_files.management.commands',
        'database_files.migrations',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)