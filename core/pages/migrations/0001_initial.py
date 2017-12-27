# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-27 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155, verbose_name='title')),
                ('slug', models.CharField(max_length=155, verbose_name='slug')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('pub_date', models.DateTimeField(blank=True, null=True, verbose_name='publication date')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('is_in_nav', models.BooleanField(default=False, verbose_name='is in navigation')),
                ('overwrite_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='overwrite url')),
                ('meta_title', models.CharField(blank=True, max_length=255, verbose_name='meta title')),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='meta description')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, verbose_name='meta keywords')),
                ('ordering', models.IntegerField(default=0)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pages.Page')),
            ],
        ),
        migrations.CreateModel(
            name='PageApplicationContent',
            fields=[
                ('applicationcontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='contents.ApplicationContent')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages_pageapplicationcontent_set', to='pages.Page')),
            ],
            options={
                'verbose_name': 'application content',
                'verbose_name_plural': 'application contents',
                'ordering': ['ordering'],
            },
            bases=('contents.applicationcontent',),
        ),
        migrations.CreateModel(
            name='PageImageContent',
            fields=[
                ('imagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='contents.ImageContent')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages_pageimagecontent_set', to='pages.Page')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'ordering': ['ordering'],
            },
            bases=('contents.imagecontent',),
        ),
        migrations.CreateModel(
            name='PageRichTextContent',
            fields=[
                ('richtextcontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='contents.RichTextContent')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages_pagerichtextcontent_set', to='pages.Page')),
            ],
            options={
                'verbose_name': 'rich text',
                'verbose_name_plural': 'rich texts',
                'ordering': ['ordering'],
            },
            bases=('contents.richtextcontent',),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('parent', 'slug')]),
        ),
    ]
