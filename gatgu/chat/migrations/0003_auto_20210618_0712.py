# Generated by Django 3.1 on 2021-06-18 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20210608_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantprofile',
            name='wish_price',
            field=models.IntegerField(default=0),
        ),
    ]