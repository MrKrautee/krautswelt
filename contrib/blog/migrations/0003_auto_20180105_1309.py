# Generated by Django 2.0.1 on 2018-01-05 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180102_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='related_entries',
        ),
        migrations.AddField(
            model_name='article',
            name='related_articles',
            field=models.ManyToManyField(blank=True, related_name='_article_related_articles_+', to='blog.Article'),
        ),
        migrations.AlterField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='articles', to='blog.Category', verbose_name='categories'),
        ),
    ]