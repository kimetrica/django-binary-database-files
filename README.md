Django Binary Database Files
============================

[![](https://img.shields.io/pypi/v/django-binary-database-files.svg)](https://pypi.python.org/pypi/django-binary-database-files) [![Build Status](https://img.shields.io/travis/kimetrica/django-binary-database-files.svg?branch=master)](https://travis-ci.org/kimetrica/django-binary-database-files/) [![](https://pyup.io/repos/github/kimetrica/django-binary-database-files/shield.svg)](https://pyup.io/repos/github/kimetrica/django-binary-database-files)

This is a storage system for Django that stores uploaded
files in binary fields in the database. Files can be served from the database
(usually a bad idea), the file system, or a CDN.

WARNING: It is generally a bad idea to serve static files from Django,
but there are some valid use cases. If your Django app is behind a caching
reverse proxy and you need to scale your application servers, it may be
simpler to store files in the database.

Based upon django-database-files by [Kimetrica](https://github.com/kimetrica/django-database-files), [rhunwicks](https://github.com/rhunwicks/django-database-files), [chrisspen](https://github.com/chrisspen/django-database-files-3000), [bfirsh](https://github.com/bfirsh/django-database-files) but updated to work with Django 2.2-4.0, Python 3.6+ and to use a binary field for storage.

Requires:

  * Django 2.2 - 4.0

Installation
------------

Simply install via pip with:

    pip install django-binary-database-files

Usage
-----

In `settings.py`, add `binary_database_files` to your `INSTALLED_APPS` and add
this line:

    DEFAULT_FILE_STORAGE = 'binary_database_files.storage.DatabaseStorage'

Note, the `upload_to` parameter is still used to synchronize the files stored
in the database with those on the file system, so new and existing fields
should still have a value that makes sense from your base media directory.

If you are adding the package to an existing Django installation with pre-existing
files, run:

    python manage.py database_files_load

Additionally, if you want to export all files in the database back to the file
system, run:

    python manage.py database_files_dump

Note, that when a field referencing a file is cleared, the corresponding file
in the database and on the file system will not be automatically deleted.
To delete all files in the database and file system not referenced by any model
fields, run:

    python manage.py database_files_cleanup

Settings
-------

* `DB_FILES_AUTO_EXPORT_DB_TO_FS` = `True`|`False` (default `True`)

    If true, when a file is uploaded or read from the database, a copy will be
    exported to your media directory corresponding to the FileField's upload_to
    path, just as it would with the default Django file storage.

    If false, the file will only exist in the database.

* `DATABASE_FILES_URL_METHOD` = `'URL_METHOD_1'`|`'URL_METHOD_2'` (default `'URL_METHOD_1'`)

    Defines the method to use when rendering the web-accessible URL for a file.

    If `URL_METHOD_1`, assumes all files have been exported to the filesystem and
    uses the path corresponding to your `settings.MEDIA_URL`.

    If `URL_METHOD_2`, uses the URL bound to the `database_file` view
    to dynamically lookup and serve files from the filesystem or database.

    In this case, you will also need to updates your `urls.py` to include the view
    that serves the files:

        urlpatterns = [
            # ... the rest of your URLconf goes here ...

            # Serve Database Files directly
            path(r"", include("binary_database_files.urls")),
        ]

* `DATABASE_FILES_BASE_URL`

    Allows the `url` method of the storage backend to return an absolute URL if provided.


Development
-----------

Code should be linted with:

    ./pep8.sh

Tests require the Python development headers to be installed, which you can install on Ubuntu with:

    sudo apt-get install python3.12-minimal python3.12-dev

To run unittests across multiple Python versions, install:

    sudo apt-get install python3.10-minimal python3.10-dev python3.11-minimal python3.11-dev python3.12-minimal python3.12-dev

To run all [tests](http://tox.readthedocs.org/en/latest/):

    export TESTNAME=; tox

To run tests for a specific environment (e.g. Python 3.12 with Django 5.0):

    export TESTNAME=; tox -e py312-django50

To run a specific test:

    export TESTNAME=.test_adding_file; tox -e py312-django50

To build and deploy a versioned package to PyPI, verify [all unittests are passing](https://travis-ci.com/kimetrica/django-binary-database-files/), then increase (and commit) the version number in `binary_database_files/__init__.py` and then run:

    python setup.py sdist bdist_wheel
    twine check dist/*
    twine upload dist/*
    
