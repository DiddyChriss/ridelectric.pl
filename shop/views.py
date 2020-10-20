from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse
from shop.models import *
from shop.forms import *
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views import View
from django.views.generic import (
    ListView,
    DetailView
    )

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Class area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Shop_post_View():                                 # all POST class
    def post(self,request, pk=None,  *args, **kwargs):
        form = Search_form(self.request.POST or None)
        pay_form = PaymentForms(self.request.POST or None)
        user_form = UserForms(self.request.POST or None)
        queryset_cart_all_users = OrderItem.objects.all()
        try:
            if request.user.is_authenticated:
                customer = request.user.customer
            else:
                device = request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            queryset_cart = []
            for user_item in queryset_cart_all_users:
                if user_item.order == order:
                    queryset_cart.append(user_item)
        except:
            queryset_cart = []

        if form.is_bound and form.is_valid():  # use seerch
            form_value = form.cleaned_data['search_product']
            queryset = Product.objects.filter(title_product__icontains=form_value)
            messages.info(request, 'Znalezione produkty:', extra_tags="info")
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
        elif 'pay' in self.request.POST:                                # go to payment
            return HttpResponseRedirect('/sklep/koszyk/zaplac/')
        elif 'pay_payment' in self.request.POST and pay_form.is_bound and pay_form.is_valid():  # pay button
            shoppingadress = pay_form.save(commit=False)
            shoppingadress.customer = customer
            shoppingadress.order = order
            shoppingadress.save()
            return redirect('/sklep/koszyk/zaplac/paypal/')
        elif 'register' in self.request.POST:                           # register button
            user_question = user_form.save(commit=False)
            try:
                Customer.objects.get(email=user_question.email)
                messages.error(request, 'Konto o podanym adresie emial już istnieje, zaloguj się!', extra_tags="error")
                return HttpResponseRedirect('/sklep/rejestracja')
            except:
                user_question.save()
                messages.info(request,
                              'Konto o nazwie: {}, zostało utworzone, zaloguj się!'.format(user_question.name),
                              extra_tags="info"
                              )
                return HttpResponseRedirect('/sklep/logowanie')


        form = Search_form()
        context = {
            'form': form,
            'user_form': user_form,
            'shop_products': queryset,
            'shop_products_cart': len(queryset_cart),
            'shop_products_cart_list': queryset_cart,
            'order': order
        }

        return render(self.request, 'shop/shop_search.html', context)





class Shop_get_View():                                                  #all get class
    def get(self,request, pk=None,  *args, **kwargs):
        form = Search_form()
        pay_form = PaymentForms()
        user_form = UserForms()

        queryset = Product.objects.all()
        queryset_cart_all_users = OrderItem.objects.all()
        Customer.objects.get_or_create(device='is_anonymous')
        order = ''
        customer = ''
        try:
            if request.user.is_authenticated:
                customer = request.user.customer
            else:
                device = request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            queryset_cart = []
            for user_item in queryset_cart_all_users:
                if user_item.order == order:
                    queryset_cart.append(user_item)
        except:
            queryset_cart = []

        context = {
            'form': form,
            'pay_form': pay_form,
            'user_form': user_form,
            'shop_products': queryset,
            'shop_products_cart': len(queryset_cart),
            'shop_products_cart_list': queryset_cart,
            'order': order,
            'customer': customer,
            'customer_count': len(str(customer))
        }
        return render(self.request, self.template_name, context)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Class area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Template/Search area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


class ShopAllListView(Shop_get_View, Shop_post_View, View):                              # All products from shop
    template_name = 'shop/shop.html'

class Shop_Product_DetailView(Shop_post_View, View):                       # Detail products from shop
    template_name = 'shop/shop_detail.html'

    def get(self, request, pk=None, *args, **kwargs):
        form = Search_form()
        queryset_cart_all_users = OrderItem.objects.all()
        try:
            if request.user.is_authenticated:
                customer = request.user.customer
            else:
                device = request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            queryset_cart = []
            for user_item in queryset_cart_all_users:
                if user_item.order == order:
                    queryset_cart.append(user_item)
        except:
            queryset_cart = []

        context = {
            'form': form,
            'shop_products_cart': len(queryset_cart),
        }
        if pk is not None:
            object = get_object_or_404(Product, pk=pk)
            context['object'] = object

        return render(request, self.template_name, context)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Template/Search area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Shopping cart area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Shop_Cart_View(Shop_get_View, Shop_post_View, View):
    template_name = 'shop/shop_cart.html'

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Shopping cart area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Payment area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Shop_Payment_View(Shop_get_View, Shop_post_View, View):
    template_name = 'shop/shop_payment.html'

class Shop_PayPal_View(Shop_get_View, View):
    template_name = 'shop/shop_paypal.html'

class Shop_PayPal_End_View(View):
    template_name = 'shop/shop_paypal_end.html'
    def get(self,request, pk=None,  *args, **kwargs):
        Customer.objects.get_or_create(device='is_anonymous')
        order = ''
        try:
            if request.user.is_authenticated:
                customer = request.user.customer
            else:
                device = request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        except:
            pass
        order.complete = True
        order.save()
        return render(self.request, self.template_name)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Payment area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Login area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Shop_Login_View(Shop_get_View, View):
    template_name = 'shop/shop_login.html'

class Shop_Register_View(Shop_post_View, Shop_get_View, View):
    template_name = 'shop/shop_register.html'

class Shop_Reset_Password_View(Shop_get_View, View):
    template_name = 'shop/shop_resetpassword.html'

class Shop_User_View(Shop_get_View, View):
    template_name = 'shop/shop_user.html'

class Shop_Logoff_View(View):
    def get(self, request, pk=None, *args, **kwargs):
        print('twoja stara')
        #######################################################
        ############### funkcja wylogowania####################
        #######################################################
        return HttpResponseRedirect('/sklep/logowanie')


class emailsent(Shop_get_View, View):                           ######usun#####################################
    template_name = 'shop/shop_send_email.html'

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Login area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>