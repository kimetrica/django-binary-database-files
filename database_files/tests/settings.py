import os, sys

PROJECT_DIR = os.path.dirname(__file__)

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        # Don't do this. It dramatically slows down the test.
#        'NAME': '/tmp/database_files.db',
#        'TEST_NAME': '/tmp/database_files.db',
    }
}

ROOT_URLCONF = 'database_files.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'database_files',
    'database_files.tests',
    'south',
]

DEFAULT_FILE_STORAGE = 'database_files.storage.DatabaseStorage'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# Run our South migrations during unittesting.
SOUTH_TESTS_MIGRATE = True

USE_TZ = True

SECRET_KEY = 'secret'
