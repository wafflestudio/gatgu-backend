# Generated by Django 3.1 on 2021-02-22 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50)),
                ('description', models.TextField(db_index=True)),
                ('location', models.CharField(max_length=50)),
                ('product_url', models.URLField()),
                ('thumbnail_url', models.URLField()),
                ('people_min', models.PositiveSmallIntegerField()),
                ('price_min', models.PositiveIntegerField()),
                ('time_max', models.DateTimeField(null=True)),
                ('time_remaining', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('need_type', models.PositiveSmallIntegerField(choices=[(1, 'people'), (2, 'money')], default=1, null=True)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
