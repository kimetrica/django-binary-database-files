import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField, ImageField

from database_files.models import File

from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-w', '--overwrite', action='store_true',
            dest='overwrite', default=False,
            help='If given, overwrites any existing files.'),
    )
    help = 'Dumps all files in the database referenced by FileFields ' + \
        'or ImageFields onto the filesystem in the directory specified by ' + \
        'MEDIA_ROOT.'

    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        try:
            q = File.objects.all()
            total = q.count()
            i = 0
            for file in q:
                i += 1
                print '%i of %i' % (i, total)
                fqfn = os.path.join(settings.MEDIA_ROOT, file.name)
                fqfn = os.path.normpath(fqfn)
                if os.path.isfile(fqfn) and not options['overwrite']:
                    continue
                dirs,fn = os.path.split(fqfn)
                if not os.path.isdir(dirs):
                    os.makedirs(dirs)
                open(fqfn, 'wb').write(file.content)
        finally:
            settings.DEBUG = tmp_debug
            