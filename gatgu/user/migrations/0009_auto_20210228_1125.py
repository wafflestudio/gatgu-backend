# Generated by Django 3.1 on 2021-02-28 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_merge_20210228_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]
