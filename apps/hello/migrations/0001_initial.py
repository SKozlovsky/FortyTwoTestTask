# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'hello_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('con_email', self.gf('django.db.models.fields.EmailField')(max_length=79)),
            ('con_jabbber', self.gf('django.db.models.fields.EmailField')(max_length=79)),
            ('con_skype', self.gf('django.db.models.fields.CharField')(max_length=79)),
            ('bio', self.gf('django.db.models.fields.TextField')(max_length=400)),
            ('con_other', self.gf('django.db.models.fields.TextField')(max_length=400, blank=True)),
        ))
        db.send_create_signal(u'hello', ['Person'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'hello_person')


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