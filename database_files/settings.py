import os

from django.conf import settings
from django.core.urlresolvers import reverse

# If true, when file objects are created, they will be automatically copied
# to the local file system for faster serving.
settings.DB_FILES_AUTO_EXPORT_DB_TO_FS = getattr(
    settings,
    'DB_FILES_AUTO_EXPORT_DB_TO_FS',
    True)

def URL_METHOD_1(name):
    """
    Construct file URL based on media URL.
    """
    return os.path.join(settings.MEDIA_URL, name)

def URL_METHOD_2(name):
    """
    Construct file URL based on configured URL pattern.
    """
    return reverse('database_file', kwargs={'name': name})

URL_METHODS = (
    ('URL_METHOD_1', URL_METHOD_1),
    ('URL_METHOD_2', URL_METHOD_2),
)

settings.DATABASE_FILES_URL_METHOD_NAME = getattr(
    settings,
    'DATABASE_FILES_URL_METHOD',
    'URL_METHOD_1')

if callable(settings.DATABASE_FILES_URL_METHOD_NAME):
    method = settings.DATABASE_FILES_URL_METHOD_NAME
else:
    method = dict(URL_METHODS)[settings.DATABASE_FILES_URL_METHOD_NAME]
settings.DATABASE_FILES_URL_METHOD = method

settings.DB_FILES_DEFAULT_ENFORCE_ENCODING = getattr(
    settings, 'DB_FILES_DEFAULT_ENFORCE_ENCODING', True)

settings.DB_FILES_DEFAULT_ENCODING = getattr(
    settings,
    'DB_FILES_DEFAULT_ENCODING',
    'ascii')

settings.DB_FILES_DEFAULT_ERROR_METHOD = getattr(
    settings, 'DB_FILES_DEFAULT_ERROR_METHOD', 'ignore')

settings.DB_FILES_DEFAULT_HASH_FN_TEMPLATE = getattr(
    settings, 'DB_FILES_DEFAULT_HASH_FN_TEMPLATE', '%s.hash')
