# Generated by Django 2.2.12 on 2020-09-24 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_ev_7kw_categories_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ev_7kw',
            name='categories_product',
            field=models.CharField(choices=[('E7', 'EV_7KW'), ('E2', 'EV_22KW'), ('EC', 'EV_CABLE'), ('PM', 'PV_MODULES'), ('PI', 'PV_INVERTERS'), ('PO', 'PV_OTHERS')], default='E7', max_length=2),
        ),
    ]