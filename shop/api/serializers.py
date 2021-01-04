from rest_framework import serializers
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField, ImageField, DateTimeField

from shop.models import Customer, Product, Order, OrderItem, ShoppingAddress

class ShoppingAddressSerializer(ModelSerializer):
    user = SerializerMethodField()
    class Meta:
        model   = ShoppingAddress
        fields  = [
            'pk',
            'customer',
            'user',
            'order',
            'first_name',
            'last_name',
            'email',
            'street_name',
            'street_number',
            'city',
            'zip_code',
            'comment',
        ]
        lookup_field = 'pk'

    def get_fields(self, *args, **kwargs):
        fields = super(ShoppingAddressSerializer, self).get_fields(*args, **kwargs)
        fields['customer'].read_only = True
        fields['order'].read_only = True
        return fields

    def to_representation(self, obj,  *args, **kwargs):                                      # remove selected fields
        ret = super(ShoppingAddressSerializer, self).to_representation(obj)
        ret.pop('customer')
        ret.pop('order')
        return ret

    def get_user(self, obj):                                           # user
        return str(obj.customer.user.username)



    def validate(self, data, *args, **kwargs):                                          # validation
        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)
        email = data.get("email", None)
        street_name = data.get("street_name", None)
        street_number = data.get("street_number", None)
        city = data.get("city", None)
        zip_code = data.get("zip_code", None)

        if first_name is None or last_name is None or email is None or street_name is None or street_number is None\
                or city is None or zip_code is None:
            raise serializers.ValidationError("Wypełnij puste pola!")
        return data


class OrderSerializer(ModelSerializer):
    customer = SerializerMethodField()
    order_pk = SerializerMethodField()
    date_order = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model   = Order
        fields  = [
            'pk',
            'order_pk',
            'customer',
            'complete',
            'date_order',
        ]

    def to_representation(self, obj, *args, **kwargs):  # remove selected fields
        ret = super(OrderSerializer, self).to_representation(obj)
        ret.pop('pk')
        return ret
    def get_customer(self, obj):
        return str(obj.customer.user)

    def get_order_pk(self, obj):
        return obj.pk

class OrderItemSerializer(ModelSerializer):
    product = SerializerMethodField()
    order_pk = SerializerMethodField()
    class Meta:
        model   = OrderItem
        fields  = [
            'pk',
            'order',
            'order_pk',
            'product',
            'quantity',
            'date_added',
        ]

    def get_product(self, obj):  # user
        return str(obj.product.title_product)

    def get_order_pk(self, obj):
        try:
            orderpk = obj.order.pk
        except:
            orderpk = ""
        return orderpk

    def to_representation(self, obj, *args, **kwargs):  # remove selected fields
        ret = super(OrderItemSerializer, self).to_representation(obj)
        try:
            ret.pop('order')
        except:
            pass
        return ret
