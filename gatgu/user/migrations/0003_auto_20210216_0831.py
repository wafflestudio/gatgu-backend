# Generated by Django 3.1 on 2021-02-16 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210215_0630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='phonenumber',
            new_name='phone',
        ),
    ]