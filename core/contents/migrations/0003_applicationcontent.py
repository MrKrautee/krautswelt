# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-16 23:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_auto_20171216_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('urls_conf', models.CharField(max_length=255)),
            ],
        ),
    ]