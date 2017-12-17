# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-16 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_applicationcontent'),
        ('pages', '0001_initial'),
    ]

    operations = [
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
    ]
