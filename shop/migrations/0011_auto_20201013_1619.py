# Generated by Django 2.2.12 on 2020-10-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20201013_1446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingaddress',
            old_name='name',
            new_name='firstname',
        ),
        migrations.AddField(
            model_name='shoppingaddress',
            name='lastname',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
