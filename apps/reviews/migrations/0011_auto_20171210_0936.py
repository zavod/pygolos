# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-10 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20171210_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='golos_user',
        ),
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='review',
            name='provider',
            field=models.CharField(choices=[('golos', 'golos'), ('steem', 'steem')], default='golos', max_length=255, verbose_name='provider'),
        ),
        migrations.AlterField(
            model_name='review',
            name='tags',
            field=models.CharField(blank=True, help_text='only 5 tags', max_length=255, null=True, verbose_name='tags'),
        ),
    ]
