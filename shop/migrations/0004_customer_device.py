# Generated by Django 2.2.12 on 2020-10-10 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20201009_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='device',
            field=models.CharField(max_length=200, null=True),
        ),
    ]