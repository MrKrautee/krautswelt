# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_imagecontent_css_float'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='slug-default-migration', max_length=100, verbose_name='slug'),
            preserve_default=False,
        ),
    ]