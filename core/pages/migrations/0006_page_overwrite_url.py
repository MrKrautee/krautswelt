# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-20 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_page_is_in_nav'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='overwrite_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='overwrite url'),
        ),
    ]
