django-database-files
=====================

django-database-files is a storage system for Django that stores uploaded files
in the database.

WARNING: It is generally a bad idea to serve static files from Django, 
but there are some valid use cases. If your Django app is behind a caching 
reverse proxy and you need to scale your application servers, it may be 
simpler to store files in the database.

Requires:

  * Django 1.6+ (or 1.4+ with django-binaryfield)

Installation
------------

Simply install via pip with:
        
    pip install https://github.com/rhunwicks/django-database-files/zipball/master

Usage
-----

In `settings.py`, add `database_files` to your `INSTALLED_APPS` and add
this line:

    DEFAULT_FILE_STORAGE = 'database_files.storage.DatabaseStorage'

Note, the `upload_to` parameter is still used to synchronize the files stored
in the database with those on the file system, so new and existing fields
should still have a value that makes sense from your base media directory.

If you're using South, the initial model migrations will scan through all
existing models for `FileFields` or `ImageFields` and will automatically
load them into the database.

If for any reason you want to re-run this bulk import task, run:

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

* `DATABASE_FILES_URL_METHOD` = `URL_METHOD_1`|`URL_METHOD_1` (default `URL_METHOD_1`)
    
    Defines the method to use when rendering the web-accessible URL for a file.
    
    If `URL_METHOD_1`, assumes all files have been exported to the filesystem and
    uses the path corresponding to your `settings.MEDIA_URL`.
    
    If `URL_METHOD_2`, uses the URL bound to the `database_file` view
    to dynamically lookup and serve files from the filesystem or database.

    In this case, you will also need to updates your `urls.py` to include the view
that serves the files:

        urlpatterns = patterns('',
            # ... the rest of your URLconf goes here ...
        
            # Serve Database Files directly
            url(r'', include('database_files.urls')),
        )
    

Development
-----------

You can run unittests with:

    python setup.py test

You can run unittests for a specific Python version using the `pv` parameter
like:

    python setup.py test --pv=3.2
    