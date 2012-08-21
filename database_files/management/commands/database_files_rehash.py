from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from database_files.models import File

class Command(BaseCommand):
    args = ''
    help = 'Regenerates hashes for all files.'
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
            total = q.count()
            i = 1
            for f in q:
                print '%i of %i: %s' % (i, total, f.name)
                f._content_hash = None
                f.save()
                i += 1
        finally:
            settings.DEBUG = tmp_debug
