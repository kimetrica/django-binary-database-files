import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField, ImageField, get_models

from optparse import make_option

class Command(BaseCommand):
    args = ''
    help = 'Loads all files on the filesystem referenced by FileFields ' + \
        'or ImageFields into the database. This should only need to be ' + \
        'done once, when initially migrating a legacy system.'

    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        try:
            broken = 0 # Number of db records referencing missing files.
            for model in get_models():
               for field in model._meta.fields:
                    if not isinstance(field, (FileField, ImageField)):
                        continue
                    print model.__name__, field.name
                    # Ignore records with null or empty string values.
                    q = {'%s__isnull'%field.name:False}
                    xq = {field.name:''}
                    for row in model.objects.filter(**q).exclude(**xq):
                        try:
                            file = getattr(row, field.name)
                            if file is None:
                                continue
                            if not file.name:
                                continue
                            if file.path and not os.path.isfile(file.path):
                                broken += 1
                                continue
                            file.read()
                            row.save()
                        except IOError:
                            broken += 1
            print '-'*80
            print '%i broken' % (broken,)
        finally:
            settings.DEBUG = tmp_debug
