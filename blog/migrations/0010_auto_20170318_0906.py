# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 09:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170316_1927'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EntryComment',
            new_name='Comments',
        ),
    ]
