# Generated by Django 3.1 on 2021-06-08 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderchat',
            name='order_status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'WAITING_MEMBERS'), (2, 'WAITING_PAY'), (3, 'WAITING_PARCELS'), (4, 'GATGU_COMPLETE')], default=1, null=True),
        ),
    ]
