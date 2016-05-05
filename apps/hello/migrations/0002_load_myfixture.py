# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        from django.core.management import call_command
        call_command("loaddata", "me.json")
        call_command("loaddata", "admin.json")

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'hello.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'con_email': ('django.db.models.fields.EmailField', [], {'max_length': '79'}),
            'con_jabbber': ('django.db.models.fields.EmailField', [], {'max_length': '79'}),
            'con_other': ('django.db.models.fields.TextField', [], {'max_length': '400', 'blank': 'True'}),
            'con_skype': ('django.db.models.fields.CharField', [], {'max_length': '79'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['hello']
    symmetrical = True
