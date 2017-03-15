# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 11:04
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=100, verbose_name='slug')),
                ('pub_date', models.DateTimeField(verbose_name='publication date')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('last_change', models.DateTimeField(auto_now=True, verbose_name='last change date')),
                ('is_featured', models.BooleanField(default=False, verbose_name='is featured')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ImageContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('caption', models.CharField(blank=True, max_length=200, verbose_name='caption')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_imagecontent_set', to='blog.BlogEntry')),
            ],
            options={
                'abstract': False,
                'ordering': ['ordering'],
            },
            bases=(blog.models.Image, models.Model),
        ),
        migrations.CreateModel(
            name='RichTextContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_richtextcontent_set', to='blog.BlogEntry')),
            ],
            options={
                'abstract': False,
                'ordering': ['ordering'],
            },
            bases=(blog.models.RichText, models.Model),
        ),
        migrations.AddField(
            model_name='blogentry',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='blogentries', to='blog.Category', verbose_name='categories'),
        ),
    ]
