# Generated by Django 2.0.1 on 2018-01-09 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20180109_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='template',
            name='path',
            field=models.CharField(max_length=255, unique=True, verbose_name='path'),
        ),
    ]