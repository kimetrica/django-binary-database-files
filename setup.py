#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages, Command

import database_files

def get_reqs(test=False):
    reqs = [
        'Django>=1.4',
        'six>=1.7.2',
    ]
    if test:
        reqs.append('South>=0.8.4')
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
        self.virtual_env_dir = './.env%s'
        self.pv = 0
        self.versions = [2.7, 3]
        
    def finalize_options(self):
        pass
    
    def build_virtualenv(self, pv):
        virtual_env_dir = self.virtual_env_dir % pv
        kwargs = dict(virtual_env_dir=virtual_env_dir, pv=pv)
        if not os.path.isdir(virtual_env_dir):
            cmd = 'virtualenv -p /usr/bin/python{pv} {virtual_env_dir}'.format(**kwargs)
            #print(cmd)
            os.system(cmd)
            
            cmd = '. {virtual_env_dir}/bin/activate; easy_install -U distribute; deactivate'.format(**kwargs)
            os.system(cmd)
            
            for package in get_reqs(test=True):
                kwargs['package'] = package
                cmd = '. {virtual_env_dir}/bin/activate; pip install -U {package}; deactivate'.format(**kwargs)
                #print(cmd)
                os.system(cmd)
    
    def run(self):
        versions = self.versions
        if self.pv:
            versions = [self.pv]
        
        for pv in versions:
            
            self.build_virtualenv(pv)
            kwargs = dict(pv=pv, name=self.name)
                
            if self.name:
                cmd = '. ./.env{pv}/bin/activate; django-admin.py test --pythonpath=. --settings=database_files.tests.settings database_files.tests.tests.{name}; deactivate'.format(**kwargs)
            else:
                cmd = '. ./.env{pv}/bin/activate; django-admin.py test --pythonpath=. --settings=database_files.tests.settings database_files.tests; deactivate'.format(**kwargs)

            print(cmd)
            ret = os.system(cmd)
            if ret:
                return

setup(
    name='django-database-files',
    version=database_files.__version__,
    description='A storage system for Django that stores uploaded files in both the database and file system.',
    author='Ben Firshman',
    author_email='ben@firshman.co.uk',
    url='http://github.com/bfirsh/django-database-files/',
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
    ],
    install_requires = get_reqs(),
    cmdclass={
        'test': TestCommand,
    },
)
