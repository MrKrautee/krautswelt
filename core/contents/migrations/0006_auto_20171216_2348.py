# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-16 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0005_applicationcontent_urls_conf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationcontent',
            name='urls_conf',
            field=models.CharField(choices=[('blog.urls', 'Blog')], max_length=100),
        ),
    ]