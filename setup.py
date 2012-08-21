#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from distutils.core import setup, Command
import database_files

def get_reqs(reqs=[]):
    # optparse is included with Python <= 2.7, but has been deprecated in favor
    # of argparse.  We try to import argparse and if we can't, then we'll add
    # it to the requirements
    try:
        import argparse
    except ImportError:
        reqs.append("argparse>=1.1")
    return reqs

class TestCommand(Command):
    description = "Runs unittests."
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('django-admin.py test --pythonpath=. --settings=database_files.tests.settings tests')
        #os.system('django-admin.py test --pythonpath=. --settings=database_files.tests.settings tests.DatabaseFilesTestCase.test_hash')

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
    requires = ["Django (>=1.4)",],
    cmdclass={
        'test': TestCommand,
    },
)