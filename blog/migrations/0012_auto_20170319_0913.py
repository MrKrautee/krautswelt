# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20170318_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='notify_new_comment',
            field=models.BooleanField(default=False, verbose_name='notify me for new comments'),
        ),
        migrations.AddField(
            model_name='comment',
            name='notify_new_entry',
            field=models.BooleanField(default=False, verbose_name='notify me for new blog entries'),
        ),
        migrations.AddField(
            model_name='comment',
            name='website',
            field=models.URLField(default='google.de', verbose_name='website'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email'),
        ),
    ]