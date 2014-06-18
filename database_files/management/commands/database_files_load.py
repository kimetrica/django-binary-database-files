from __future__ import print_function

import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField, ImageField, get_models

from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-m', '--models',
            dest='models', default='',
            help='A list of models to search for file fields. Default is all.'),
    )
    help = 'Loads all files on the filesystem referenced by FileFields ' + \
        'or ImageFields into the database. This should only need to be ' + \
        'done once, when initially migrating a legacy system.'

    def handle(self, *args, **options):
        show_files = int(options.get('verbosity', 1)) >= 2
        all_models = [
            _.lower().strip()
            for _ in options.get('models', '').split()
            if _.strip()
        ]
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        try:
            broken = 0 # Number of db records referencing missing files.
            for model in get_models():
                key = "%s.%s" % (model._meta.app_label,model._meta.module_name)
                key = key.lower()
                if all_models and key not in all_models:
                    continue
                for field in model._meta.fields:
                    if not isinstance(field, (FileField, ImageField)):
                        continue
                    if show_files:
                        print(model.__name__, field.name)
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
                            if show_files:
                                print("\t",file.name)
                            if file.path and not os.path.isfile(file.path):
                                if show_files:
                                    print("Broken:",file.name)
                                broken += 1
                                continue
                            file.read()
                            row.save()
                        except IOError:
                            broken += 1
            if show_files:
                print('-'*80)
                print('%i broken' % (broken,))
        finally:
            settings.DEBUG = tmp_debug
