import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField, ImageField, get_models

from database_files.models import File

class Command(BaseCommand):
    args = ''
    help = 'Deletes all files in the database that are not referenced by ' + \
        'any model fields.'

    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        names = set()
        try:
            for model in get_models():
               for field in model._meta.fields:
                    if not isinstance(field, (FileField, ImageField)):
                        continue
                    # Ignore records with null or empty string values.
                    q = {'%s__isnull'%field.name:False}
                    xq = {field.name:''}
                    for row in model.objects.filter(**q).exclude(**xq):
                        file = getattr(row, field.name)
                        if file is None:
                            continue
                        if not file.name:
                            continue
                        names.add(file.name)
            # Find all database files with names not in our list.
            orphan_files = File.objects.exclude(name__in=names)
            for f in orphan_files:
                print 'Deleting %s...' % (f.name,)
                default_storage.delete(f.name)
        finally:
            settings.DEBUG = tmp_debug
