# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-10 09:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20171210_0435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewimage',
            name='review',
        ),
        migrations.DeleteModel(
            name='ReviewImage',
        ),
    ]
