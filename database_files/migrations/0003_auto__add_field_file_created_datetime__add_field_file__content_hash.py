# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils import timezone

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'File.created_datetime'
        db.add_column('database_files_file', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now, db_index=True),
                      keep_default=False)

        # Adding field 'File._content_hash'
        db.add_column('database_files_file', '_content_hash',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_column='content_hash', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'File.created_datetime'
        db.delete_column('database_files_file', 'created_datetime')

        # Deleting field 'File._content_hash'
        db.delete_column('database_files_file', 'content_hash')


    models = {
        'database_files.file': {
            'Meta': {'object_name': 'File'},
            '_content': ('django.db.models.fields.TextField', [], {'db_column': "'content'"}),
            '_content_hash': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_column': "'content_hash'", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['database_files']