# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-10 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('value', models.EmailField(default='example@example.de', max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FloatSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('value', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IntegerSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('value', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]