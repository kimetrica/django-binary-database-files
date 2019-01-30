# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.apps import AppConfig


class DatabaseFilesAppConfig(AppConfig):
    """ AppConfig to make database_files compatible with 1.7+ app loading """
    name = 'database_files'
    label = 'database_files'
    verbose_name = 'django-database-files'
