# Generated by Django 3.1 on 2021-06-21 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_auto_20210620_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleimage',
            name='img_url',
            field=models.URLField(default='www.naver.com'),
        ),
    ]
