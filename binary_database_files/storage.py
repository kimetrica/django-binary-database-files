# -*- coding: utf-8 -*-
"""Custom storage backend that stores files in the database to facilitate scaling."""
from __future__ import unicode_literals, division
import os
from io import UnsupportedOperation

import six

from django.conf import settings
from django.core import files
from django.core.files.storage import FileSystemStorage

from binary_database_files import models
from binary_database_files import utils
from binary_database_files import settings as _settings


class DatabaseStorage(FileSystemStorage):
    """Subclass of FileSystemStorage that implements the necessary methods to use the database for files."""

    def __init__(self, *args, **kwargs):
        """Override __init__ to allow passing of base_url parameter to be able to resolve to absolute URL."""
        super(DatabaseStorage, self).__init__(*args, **kwargs)
        # we check first if base_url has been passed to __init__, if not we try settings and finally fall back to ''
        self._base_url = (kwargs.get('base_url') or settings.DATABASE_FILES_BASE_URL
                          if hasattr(settings, 'DATABASE_FILES_BASE_URL') else '')

    def _generate_name(self, name, pk):
        """Replace the filename with the specified pk and removes any dir."""
        # dir_name, file_name = os.path.split(name)
        # file_root, file_ext = os.path.splitext(file_name)
        # return '%s%s' % (pk, file_name)
        return name

    def _open(self, name, mode='rb'):
        """Open file with filename `name` from the database."""
        try:
            # Load file from database.
            f = models.File.objects.get_from_name(name)
            content = f.content
            size = f.size
            if _settings.DB_FILES_AUTO_EXPORT_DB_TO_FS and not utils.is_fresh(f.name, f.content_hash):
                # Automatically write the file to the filesystem
                # if it's missing and exists in the database.
                # This happens if we're using multiple web servers connected
                # to a common databaes behind a load balancer.
                # One user might upload a file from one web server, and then
                # another might access if from another server.
                utils.write_file(f.name, f.content)
        except models.File.DoesNotExist:
            # If not yet in the database, check the local file system
            # and load it into the database if present.
            fqfn = self.path(name)
            if os.path.isfile(fqfn):
                # print('Loading file into database.')
                self._save(name, open(fqfn, mode))
                fh = super(DatabaseStorage, self)._open(name, mode)
                content = fh.read()
                size = fh.size
            else:
                # Otherwise we don't know where the file is so we return an
                # empty file
                size = 0
                content = b''
        # Normalize the content to a new file object.
        fh = six.BytesIO(content)
        fh.name = name
        fh.mode = mode
        fh.size = size
        o = files.File(fh)
        return o

    def _save(self, name, content):
        """Save file with filename `name` and given content to the database."""
        full_path = self.path(name)
        # ZipExtFile advertises seek() but can raise UnsupportedOperation
        try:
            content.seek(0)
        except UnsupportedOperation:
            pass
        content = content.read()
        size = len(content)
        f = models.File.objects.create(
            content=content,
            size=size,
            name=name,
        )
        # Automatically write the change to the local file system.
        if _settings.DB_FILES_AUTO_EXPORT_DB_TO_FS:
            utils.write_file(name, content, overwrite=True)
        # @TODO: add callback to handle custom save behavior?
        return self._generate_name(name, f.pk)

    def exists(self, name):
        """Return True if a file with the given filename exists in the database. Return False otherwise."""
        if models.File.objects.filter(name=name).exists():
            return True
        return super(DatabaseStorage, self).exists(name)

    def delete(self, name):
        """Delete the file with filename `name` from the database and filesystem."""
        try:
            models.File.objects.get_from_name(name).delete()
            hash_fn = utils.get_hash_fn(name)
            if os.path.isfile(hash_fn):
                os.remove(hash_fn)
        except models.File.DoesNotExist:
            pass
        return super(DatabaseStorage, self).delete(name)

    def url(self, name):
        """Return the web-accessible URL for the file with filename `name`.

        settings.DATABASE_FILES_URL_METHOD(name) will return a relative URL. So we have to try to get the absolute url
        for the file. If self._base_url hasn't been set we will return the relative URL (by prepending just '').
        We could also raise an error like the SFTP backend of django-storages is doing, but the relative URL is the
        previous behavior so we fall back to that.
        """
        return '{}{}'.format(self._base_url, settings.DATABASE_FILES_URL_METHOD(name))

    def size(self, name):
        """Return the size of the file with filename `name` in bytes."""
        try:
            return models.File.objects.get_from_name(name).size
        except models.File.DoesNotExist:
            return super(DatabaseStorage, self).size(name)
