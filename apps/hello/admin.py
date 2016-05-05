# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Person


class AdmPersone(admin.ModelAdmin):
    fieldsets = [('Basic information',
                  {'fields': ['first_name', 'last_name', 'birth_date']}),
                 ('Contacts',
                  {'fields': ['con_email', 'con_jabbber', 'con_skype']}),
                 ('Other Contacts',
                  {'fields': ['con_other'], 'classes': ['collapse']}),
                 ('Bio', {'fields': ['bio']})]

admin.site.register(Person, AdmPersone)
