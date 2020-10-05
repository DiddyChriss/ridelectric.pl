# Generated by Django 2.2.12 on 2020-10-01 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_delete_search_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='shop_products_cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_cart', models.CharField(max_length=40, null=True)),
                ('date_cart', models.DateTimeField(auto_now=True)),
                ('description_cart', models.TextField()),
                ('price_cart', models.DecimalField(decimal_places=2, default=True, max_digits=20)),
                ('image_cart', models.FileField(null=True, upload_to='upload/')),
            ],
        ),
    ]