# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-16 23:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_applicationcontent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationcontent',
            name='name',
        ),
        migrations.RemoveField(
            model_name='applicationcontent',
            name='urls_conf',
        ),
    ]