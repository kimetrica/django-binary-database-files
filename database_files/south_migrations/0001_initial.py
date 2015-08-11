# encoding: utf-8
import datetime

from django.core.management import call_command
from django.db import models

from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'File'
        db.create_table('database_files_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('_content', self.gf('django.db.models.fields.TextField')(db_column='content')),
        ))
        db.send_create_signal('database_files', ['File'])

    def backwards(self, orm):
        
        # Deleting model 'File'
        db.delete_table('database_files_file')

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
