# Generated by Django 3.1 on 2021-03-08 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participantprofile',
            old_name='order',
            new_name='order_chat',
        ),
        migrations.AlterUniqueTogether(
            name='participantprofile',
            unique_together=set(),
        ),
    ]
