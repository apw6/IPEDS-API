# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-20 07:52
from __future__ import unicode_literals

from django.db import migrations, models

import csv
def add_data(apps, schema_editor):
    with open('./ipeds_import/IPEDS-API/base_names.txt') as base_names:
        for name in base_names:
            name = str(name).strip()
            model = apps.get_model('ipeds_import', '{}_model'.format(name))
            fields = [f.name for f in model._meta.get_fields()]
            with open('./ipeds_import/IPEDS-API/csv/{}.csv'.format(name)) as csvFile:
                # column_names = filter(lambda field: field not in ['id'], get_all_field_names(model))
                column_names = filter(lambda field: field not in ['id'], fields)
                rows = csv.DictReader(csvFile)
                for row in rows:
                    arguments = { column: unicode(row[column], "utf-8", errors='ignore') for column in column_names }
                    model(**arguments).save()

def undo_migrate(apps, schema_editor):
    with open('./ipeds_import/toolbox/base_names.txt') as base_names:
        for name in base_names:
                name = str(name).strip()
                model = apps.get_model('ipeds_import', '{}_model'.format(name))
                model.objects.all().delete()

class Migration(migrations.Migration):
    
    dependencies = [
        ('ipeds_import', '0001_initial')
    ]

    operations = [
        migrations.RunPython(add_data, undo_migrate),
    ]