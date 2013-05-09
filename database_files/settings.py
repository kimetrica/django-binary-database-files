import os

from django.conf import settings
from django.core.urlresolvers import reverse

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

DATABASE_FILES_URL_METHOD_NAME = getattr(
    settings,
    'DATABASE_FILES_URL_METHOD',
    'URL_METHOD_1')

if callable(DATABASE_FILES_URL_METHOD_NAME):
    method = DATABASE_FILES_URL_METHOD_NAME
else:
    method = dict(URL_METHODS)[DATABASE_FILES_URL_METHOD_NAME]

DATABASE_FILES_URL_METHOD = setattr(
    settings,
    'DATABASE_FILES_URL_METHOD',
    method)
