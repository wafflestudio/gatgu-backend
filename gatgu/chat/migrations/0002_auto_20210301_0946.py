# Generated by Django 3.1 on 2021-03-01 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participantprofile',
            name='wish_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orderchat',
            name='article',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='article.article'),
        ),
    ]