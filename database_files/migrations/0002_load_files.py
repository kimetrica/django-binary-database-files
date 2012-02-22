# encoding: utf-8
import datetime

from django.core.management import call_command
from django.db import models

from south.db import db
from south.v2 import DataMigration

class Migration(DataMigration):

    def forwards(self, orm):
        # Load any files referenced by existing models into the database.
        call_command('database_files_load')

    def backwards(self, orm):
        import database_files
        database_files.models.File.objects.all().delete()

    models = {
        'database_files.file': {
            'Meta': {'object_name': 'File'},
            '_content': ('django.db.models.fields.TextField', [], {'db_column': "'content'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['database_files']
