# Generated by Django 3.1 on 2021-06-20 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_auto_20210618_0522'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArticleTag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
