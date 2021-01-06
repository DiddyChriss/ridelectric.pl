from django.contrib import messages
from django.shortcuts import get_object_or_404, HttpResponseRedirect

from rest_framework import generics, mixins, viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, TemplateHTMLRenderer, JSONRenderer


from shop.models import Customer, Product, Order, OrderItem, ShoppingAddress

from .serializers import ShoppingAddressSerializer, OrderItemSerializer, OrderSerializer

class ShoppingaddressAPIView(viewsets.ModelViewSet):
    queryset = ShoppingAddress.objects.all()
    serializer_class = ShoppingAddressSerializer
    parser_classes = [FormParser, MultiPartParser]
    renderer_classes = [TemplateHTMLRenderer,]
    template_name = 'admin/shopping_address.html'

    def list(self, request, *args, **kwargs):
        serializer_form = ''
        shoppingaddress_detial = ''
        queryset = self.filter_queryset(self.get_queryset())
        try:
            customer = Customer.objects.get(user=request.user)
            queryset = queryset.filter(customer=customer)
            page = self.paginate_queryset(queryset)
        except:
            page = None
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        pk = self.kwargs.get('pk')
        if pk:
            shoppingaddress_detial = get_object_or_404(ShoppingAddress, pk=pk)
            serializer_form = ShoppingAddressSerializer(shoppingaddress_detial)

        return Response({'serializer_data': serializer.data,
                         'serializer': serializer_form,
                         'shoppingaddress': shoppingaddress_detial,
                         })

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            messages.error(request, 'Dane użytkownika zostały zmienione', extra_tags="error")
            return HttpResponseRedirect('/sklep/api/{}/'.format(pk))
        messages.error(request, 'Aby zapisać zmiany wypełnij wszystkie pola oznaczone sybolem "*"', extra_tags="error")
        return HttpResponseRedirect('/sklep/api/{}/'.format(pk))

class OrderAPIView(viewsets.ModelViewSet):
    queryset=Order.objects.all()
    serializer_class = OrderSerializer
    parser_classes =[FormParser, MultiPartParser]
    renderer_classes =[TemplateHTMLRenderer, ]
    template_name = 'admin/user_orders.html'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            customer = Customer.objects.get(user=request.user)
            queryset = queryset.filter(customer=customer)
            page = self.paginate_queryset(queryset)
        except:
            page = None
        try:
            shoppingaddress_detial = ShoppingAddress.objects.get(customer=customer)
        except:
            shoppingaddress_detial = 0
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'serializer_data': serializer.data, 'shoppingaddress': shoppingaddress_detial,})


class OrderItemAPIView(viewsets.ModelViewSet):
    queryset=OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    parser_classes =[FormParser, MultiPartParser]
    renderer_classes =[TemplateHTMLRenderer, ]
    template_name = 'admin/user_orders_itemorders.html'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            customer = Customer.objects.get(user=request.user)
            queryset = queryset.filter(customer=customer, pk=pk)
            page = self.paginate_queryset(queryset)
        except:
            page = None
        try:
            shoppingaddress_detial = ShoppingAddress.objects.get(
                customer=customer)
        except:
            shoppingaddress_detial = 0
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        pk = self.kwargs.get('pk')
        serializer = self.get_serializer(queryset, many=True)

        return Response({'serializer_data': serializer.data, 'shoppingaddress': shoppingaddress_detial, 'pk': pk })


