#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages, Command

import database_files

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except:
    print("Warning: pypandoc module not found, could not convert "
        "Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

def get_reqs(test=False, pv=None):
    reqs = [
        'Django>=1.4',
        'six>=1.7.2',
    ]
    if test:
        #TODO:remove once Django 1.7 south integration becomes main-stream?
        if not pv:
            reqs.append('South>=1.0')
        elif pv <= 3.2:
            # Note, South dropped Python3 support after 0.8.4...
            reqs.append('South==0.8.4')
    return reqs

class TestCommand(Command):
    description = "Runs unittests."
    user_options = [
        ('name=', None,
         'Name of the specific test to run.'),
        ('virtual-env-dir=', None,
         'The location of the virtual environment to use.'),
        ('pv=', None,
         'The version of Python to use. e.g. 2.7 or 3'),
    ]
    
    def initialize_options(self):
        self.name = None
        self.virtual_env_dir = '.env%s'
        self.pv = 0
        self.versions = [
            2.7,
            3,
            #3.3,#TODO?
        ]
        
    def finalize_options(self):
        pass
    
    def build_virtualenv(self, pv):
        virtual_env_dir = self.virtual_env_dir % pv
        kwargs = dict(virtual_env_dir=virtual_env_dir, pv=pv)
        if not os.path.isdir(virtual_env_dir):
            cmd = 'virtualenv -p /usr/bin/python{pv} {virtual_env_dir}'.format(**kwargs)
            print(cmd)
            os.system(cmd)
            
            cmd = '{virtual_env_dir}/bin/easy_install -U distribute'.format(**kwargs)
            print(cmd)
            os.system(cmd)
            
            for package in get_reqs(test=True, pv=float(pv)):
                kwargs['package'] = package
                cmd = '{virtual_env_dir}/bin/pip install -U {package}'.format(**kwargs)
                print(cmd)
                os.system(cmd)
    
    def run(self):
        versions = self.versions
        if self.pv:
            versions = [self.pv]
        
        for pv in versions:
            
            self.build_virtualenv(pv)
            kwargs = dict(
                pv=pv,
                virtual_env_dir=self.virtual_env_dir % pv,
                name=self.name)
                
            if self.name:
                cmd = '{virtual_env_dir}/bin/django-admin.py test --pythonpath=. --settings=database_files.tests.settings database_files.tests.tests.{name}'.format(**kwargs)
            else:
                cmd = '{virtual_env_dir}/bin/django-admin.py test --pythonpath=. --settings=database_files.tests.settings database_files.tests'.format(**kwargs)

            print(cmd)
            ret = os.system(cmd)
            if ret:
                return

try:
    long_description = read_md('README.md')
except IOError:
    long_description = ''

setup(
    name='django-database-files-3000',
    version=database_files.__version__,
    description='A storage system for Django that stores uploaded files in both the database and file system.',
    long_description=long_description,
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='http://github.com/chrisspen/django-database-files-3000',
    packages=[
        'database_files',
        'database_files.management',
        'database_files.management.commands',
        'database_files.migrations',
    ],
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.2',
    ],
    install_requires = get_reqs(),
    cmdclass={
        'test': TestCommand,
    },
)
