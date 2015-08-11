# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import base64

from database_files import utils

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        File = orm['database_files.File']
        q = File.objects.all()
        for f in q:
            f._content_hash = utils.get_text_hash_0004(base64.b64decode(f._content))
            f.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'database_files.file': {
            'Meta': {'object_name': 'File'},
            '_content': ('django.db.models.fields.TextField', [], {'db_column': "'content'"}),
            '_content_hash': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_column': "'content_hash'", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['database_files']
    symmetrical = True
