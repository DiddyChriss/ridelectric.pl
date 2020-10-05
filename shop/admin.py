from django.contrib import admin
from shop.models import shop_products, shop_products_cart


admin.site.register(shop_products)
admin.site.register(shop_products_cart)

