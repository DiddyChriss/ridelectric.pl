from django.contrib import admin
from django.contrib.auth.models import Group

from mptt.admin import MPTTModelAdmin

from .models import *


class CustomerAdmin(admin.ModelAdmin):
    search_fields=['user__username', 'name', 'email']

class ProductAdmin(admin.ModelAdmin):
    search_fields=['title_product',]

class OrderAdmin(admin.ModelAdmin):
    search_fields=['customer__user__username', 'id']

class OrderItemAdmin(admin.ModelAdmin):
    search_fields=['product__title_product', 'order__id']

class ShoppingAddressAdmin(admin.ModelAdmin):
    search_fields=['customer__user__username', 'order__id', 'first_name', 'last_name', 'email', 'street_name', 'city']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShoppingAddress, ShoppingAddressAdmin)


admin.site.register(Category, MPTTModelAdmin)


admin.site.unregister(Group)