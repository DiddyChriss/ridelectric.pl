from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import Permission, User
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views import View
from django.views.generic import (
    ListView,
    DetailView
    )

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Class area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Shop_get_View():
    def get(self,request, pk=None,  *args, **kwargs):
        form = Search_form()
        queryset = Product.objects.all()
        queryset_cart = OrderItem.objects.all()

        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            device = request.COOKIES['device']
            customer= Customer.objects.get(device=device)
        order= Order.objects.get(customer=customer)

        context = {
            'form': form,
            'shop_products': queryset,
            'shop_products_cart': queryset_cart,
            'order': order,
        }
        return render(self.request, self.template_name, context)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Class area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Template/Search area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


class ShopAllListView(Shop_get_View, View):                              # All products from shop
    template_name = 'shop/shop.html'

    def post(self, *args, **kwargs):
        form = Search_form(self.request.POST or None)
        queryset_cart = OrderItem.objects.all()
        if form.is_valid():                                                 # use seerch
            form_value = form.cleaned_data['search_product']
            queryset = Product.objects.filter(title_product__icontains=form_value)
        else:
            form = Search_form()

        context = {
            'form': form,
            'shop_products': queryset,
            'shop_products_cart': queryset_cart
        }
        return render(self.request, 'shop/shop_search.html', context)


class Shop_Product_DetailView(View):                       # Detail products from shop
    template_name = 'shop/shop_detail.html'

    def get(self, request, pk=None, *args, **kwargs):
        form = Search_form()
        queryset_cart = OrderItem.objects.all()

        context = {
            'form': form,
            'shop_products_cart': queryset_cart
        }
        if pk is not None:
            object = get_object_or_404(Product, pk=pk)
            context['object'] = object

        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        form = Search_form(self.request.POST or None)
        queryset_cart = OrderItem.objects.all()
        if form.is_bound and form.is_valid():                                   # use seerch
            form_value = form.cleaned_data['search_product']
            queryset = Product.objects.filter(title_product__icontains=form_value)
        elif 'add_to_cart' in self.request.POST and pk is not None:   # add to shoping cart
            if request.user.is_authenticated:
                customer = request.user.customer
            else:
                device = request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            product = get_object_or_404(Product, pk=pk)
            orderitem, created = OrderItem.objects.get_or_create(order=order, product=product, quantity='1')
            if created:
                messages.info(request, 'Produkt został dodany do koszyka', extra_tags="info")
            else:
                messages.error(request, 'Produkt już znajduje się w koszyku', extra_tags="error")

            return redirect(self.request.path)
        form = Search_form()

        context = {
            'form': form,
            'shop_products': queryset,
            'shop_products_cart': queryset_cart
        }

        return render(self.request, 'shop/shop_search.html', context)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Template/Search area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Shopping cart area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Shop_Cart_View(Shop_get_View, View):                       # Detail products from shop
    template_name = 'shop/shop_cart.html'

    def post(self, request, pk=None, *args, **kwargs):
        form = Search_form(self.request.POST or None)
        queryset_cart = OrderItem.objects.all()
        if form.is_bound and form.is_valid():                       # use seerch
            form_value = form.cleaned_data['search_product']
            queryset = Product.objects.filter(title_product__icontains=form_value)
            messages.info(request, 'Znalezione produkty:', extra_tags="info")
        elif 'delete_all_in_cart' in self.request.POST:             # delete all item
            OrderItem.objects.all().delete()
            return redirect(self.request.path)
        elif 'delete_from_cart' in self.request.POST and pk is not None:  # delete one item
            OrderItem.objects.get(id=pk ).delete()
            messages.info(request, 'Produkt został usunięty', extra_tags="info")
            return HttpResponseRedirect('/sklep/koszyk/')
        elif 'plus' in self.request.POST and pk is not None:           # plus quantity of product
            item = OrderItem.objects.get(id=pk)
            item.quantity += 1
            item.save()
            return HttpResponseRedirect('/sklep/koszyk/')
        elif 'minus' in self.request.POST and pk is not None:            # minus quantity of product
            item = OrderItem.objects.get(id=pk)
            item.quantity -= 1
            if item.quantity == 0:
                item.delete()
                messages.info(request, 'Produkt został usunięty', extra_tags="info")
            else:
                item.save()
            return HttpResponseRedirect('/sklep/koszyk/')
        form = Search_form()

        context = {
            'form': form,
            'shop_products': queryset,
            'shop_products_cart': queryset_cart
        }

        return render(self.request, 'shop/shop_search.html', context)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Shopping cart area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



