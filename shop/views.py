from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from shop.models import shop_products, shop_products_cart
from shop.forms import Search_form, Quantity_form
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
        form_quantity = Quantity_form()
        queryset = shop_products.objects.all()
        queryset_cart = shop_products_cart.objects.all()

        context = {
            'form_quantity': form_quantity,
            'form': form,
            'shop_products': queryset,
            'shop_products_cart': queryset_cart
        }

        return render(self.request, self.template_name, context)


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Class area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Template/Search area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


class ShopAllListView(Shop_get_View, View):                              # All products from shop
    template_name = 'shop/shop.html'

    def post(self, *args, **kwargs):
        form = Search_form(self.request.POST or None)
        queryset_cart = shop_products_cart.objects.all()
        if form.is_valid():
            form_value = form.cleaned_data['search_product']
            queryset = shop_products.objects.filter(title_product__icontains=form_value)
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
        queryset_cart = shop_products_cart.objects.all()
        shop_product_get = shop_products.objects.get(id=pk).title_product
        shop_products_cart_title = shop_products_cart.objects.filter(title_cart=shop_product_get)

        context = {
            'form': form,
            'shop_products_cart': queryset_cart,
            'shop_products_cart_title': shop_products_cart_title
        }
        if pk is not None:
            object = get_object_or_404(shop_products, pk=pk)
            context['object'] = object
        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        form = Search_form(self.request.POST or None)
        queryset_cart = shop_products_cart.objects.all()
        if form.is_bound and form.is_valid():
            form_value = form.cleaned_data['search_product']
            queryset = shop_products.objects.filter(title_product__icontains=form_value)
        elif 'add_to_cart' in self.request.POST and pk is not None:
            shop_product_get = shop_products.objects.get(id=pk).title_product
            shop_products_cart_title = shop_products_cart.objects.filter(title_cart=shop_product_get)
            if shop_products_cart_title:
                messages.error(request,'Produkt już znajduje się w koszyku', extra_tags="error")
            else:
                messages.info(request, 'Produkt został dodany do koszyka', extra_tags="info")
                shop_products_cart.objects.create(
                    title_cart=shop_products.objects.get(id=pk).title_product,
                    description_cart=shop_products.objects.get(id=pk).description_product,
                    price_cart=shop_products.objects.get(id=pk).price_product,
                    image_cart=shop_products.objects.get(id=pk).image_product
                )
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

        form_quantity = Quantity_form(self.request.POST or None)

        queryset_cart = shop_products_cart.objects.all()
        if form.is_bound and form.is_valid():
            form_value = form.cleaned_data['search_product']
            queryset = shop_products.objects.filter(title_product__icontains=form_value)
            messages.info(request, 'Znalezione produkty:', extra_tags="info")
        elif 'delete_all_in_cart' in self.request.POST:
            shop_products_cart.objects.all().delete()
            return redirect(self.request.path)
        elif 'delete_from_cart' in self.request.POST and pk is not None:
            shop_products_cart.objects.get(id=pk ).delete()
            messages.info(request, 'Produkt został usunięty', extra_tags="info")
            return HttpResponseRedirect('/sklep/koszyk/')
        elif 'back_to_product' in self.request.POST and pk is not None:
            name_title_cart = shop_products_cart.objects.get(id=pk).title_cart
            id_product = shop_products.objects.get(title_product=name_title_cart).id
            if shop_products.objects.get(title_product=name_title_cart):
                object = get_object_or_404(shop_products, pk=id_product)
                context = {
                    'form': form,
                    'shop_products_cart': queryset_cart,
                    'object': object
                }
                return render(request, 'shop/shop_detail.html', context)

        form = Search_form()
        context = {
            'form': form,
            'shop_products': queryset,
            'shop_products_cart': queryset_cart
        }

        return render(self.request, 'shop/shop_search.html', context)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Shopping cart area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



