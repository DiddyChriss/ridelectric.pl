# Generated by Django 2.2.12 on 2020-09-24 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_cable_32a_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cable_32a',
            name='slug',
        ),
    ]
