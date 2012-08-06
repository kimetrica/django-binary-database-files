# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'File', fields ['_content_hash']
        db.create_index('database_files_file', ['content_hash'])

        # Adding index on 'File', fields ['size']
        db.create_index('database_files_file', ['size'])


    def backwards(self, orm):
        # Removing index on 'File', fields ['size']
        db.delete_index('database_files_file', ['size'])

        # Removing index on 'File', fields ['_content_hash']
        db.delete_index('database_files_file', ['content_hash'])


    models = {
        'database_files.file': {
            'Meta': {'object_name': 'File'},
            '_content': ('django.db.models.fields.TextField', [], {'db_column': "'content'"}),
            '_content_hash': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'db_column': "'content_hash'", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['database_files']