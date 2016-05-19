# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.photo'
        db.add_column(u'hello_person', 'photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.photo'
        db.delete_column(u'hello_person', 'photo')


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
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'hello.requestcollect': {
            'Meta': {'object_name': 'RequestCollect'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_method': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'r_path': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'r_status': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'r_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'r_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['hello']