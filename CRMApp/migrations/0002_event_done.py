# Generated by Django 4.2.5 on 2023-12-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRMApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]