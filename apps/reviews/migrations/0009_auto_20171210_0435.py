# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-10 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20171118_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='tags',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=1000, verbose_name='title'),
        ),
    ]
