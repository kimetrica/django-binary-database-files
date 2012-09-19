import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from database_files.models import File

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
#        make_option('-w', '--overwrite', action='store_true',
#            dest='overwrite', default=False,
#            help='If given, overwrites any existing files.'),
    )
    help = 'Dumps all files in the database referenced by FileFields ' + \
        'or ImageFields onto the filesystem in the directory specified by ' + \
        'MEDIA_ROOT.'

    def handle(self, *args, **options):
        File.dump_files(verbose=True)
        