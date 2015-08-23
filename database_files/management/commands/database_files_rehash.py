from __future__ import print_function

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from database_files.models import File

class Command(BaseCommand):
    args = '<filename 1> <filename 2> ... <filename N>'
    help = 'Regenerates hashes for files. If no filenames given, ' + \
        'rehashes everything.'
    option_list = BaseCommand.option_list + (
#        make_option('--dryrun',
#            action='store_true',
#            dest='dryrun',
#            default=False,
#            help='If given, only displays the names of orphaned files ' + \
#                'and does not delete them.'),
        )

    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        try:
            q = File.objects.all()
            if args:
                q = q.filter(name__in=args)
            total = q.count()
            i = 1
            for f in q.iterator():
                print('%i of %i: %s' % (i, total, f.name))
                f._content_hash = None
                f.save()
                i += 1
        finally:
            settings.DEBUG = tmp_debug
