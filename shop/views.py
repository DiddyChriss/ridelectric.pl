from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.template import loader
from django.core.mail import send_mail
from shop.models import *
from shop.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Class area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class ShopPostView():                                 # all POST class
    def post(self,request, pk=None,  *args, **kwargs):
        form = SearchForm(self.request.POST or None)
        pay_form = PaymentForms(self.request.POST or None)
        email_form = EmailShop(self.request.POST or None)
        queryset_cart_all_users = OrderItem.objects.all()
        category = Category.objects.all()
        shopping_address_pk = 0
        try:
            if request.user.is_authenticated:
                customer = Customer.objects.get(user=request.user)
                shopp_add_pk, create = ShoppingAddress.objects.get_or_create(customer=customer)
                shopping_address_pk = shopp_add_pk.pk
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

        if 'search' in self.request.POST and form.is_bound and form.is_valid():  # use seerch
            form_value = form.cleaned_data['search_product']
            queryset = Product.objects.filter(title_product__icontains=form_value)
            messages.info(request, 'Znalezione produkty:', extra_tags="info")

        elif 'add_to_cart' in self.request.POST and pk is not None:   # add to shoping cart
            if request.user.is_authenticated:
                user_customer = request.user
                customer, created = Customer.objects.get_or_create(user=user_customer)
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
            return HttpResponseRedirect('/sklep/koszyk/produkty/')

        elif 'plus' in self.request.POST and pk is not None:           # plus quantity of product
            item = OrderItem.objects.get(id=pk)
            item.quantity += 1
            item.save()
            return HttpResponseRedirect('/sklep/koszyk/produkty/')

        elif 'minus' in self.request.POST and pk is not None:            # minus quantity of product
            item = OrderItem.objects.get(id=pk)
            item.quantity -= 1
            if item.quantity == 0:
                item.delete()
                messages.info(request, 'Produkt został usunięty', extra_tags="info")
            else:
                item.save()
            return HttpResponseRedirect('/sklep/koszyk/produkty/')
        elif 'pay' in self.request.POST:                                # go to payment
            if request.user.is_authenticated:
                customer = Customer.objects.get(user=request.user)
                order = Order.objects.get(customer=customer, complete=False)
                sal = ShoppingAddress.objects.get(customer=customer)
                sal.order = order
                sal.save()
                if sal.first_name == None or sal.last_name == None or sal.email == None or \
                        sal.street_name == None or sal.street_number == None or sal.city == None or \
                        sal.zip_code == None:
                    messages.error(request, 'Brak informacji o wysyłce! Uzupełnij dane do wysyłki i wróć do'
                                            'koszyka aby dokończyć płatność', extra_tags="error")
                    return HttpResponseRedirect('/sklep/api/{}/'.format(sal.pk))
                else:
                    return redirect('/sklep/koszyk/zaplac/paypal/')
            else:
                return HttpResponseRedirect('/sklep/koszyk/zaplac/')
        elif 'pay_payment' in self.request.POST and pay_form.is_bound and pay_form.is_valid():  # pay button
            shoppingadress = pay_form.save(commit=False)
            shoppingadress.customer = customer
            shoppingadress.order = order
            shoppingadress.save()
            return redirect('/sklep/koszyk/zaplac/paypal/')
        elif 'register' in self.request.POST:                                    # register button
            user_form = UserForms(self.request.POST)
            if user_form.is_valid():
                username = user_form.cleaned_data.get('username')
                email = user_form.cleaned_data.get('email')
                user_form.save()

                subject = 'Dziękujemy za dokonanie rejestracji w ridelectric.pl'
                message = 'Dziękujemy za dokonanie rejestracji w ridelectric.pl'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email, 'diddychriss@gmail.com']
                html_message = loader.render_to_string('shop/login/shop_send_email.html',
                                                       {
                                                        'name': username,
                                                        'email': email,
                                                       }
                                                       )
                send_mail(subject, message, from_email, recipient_list, fail_silently=True, auth_user=None,
                          auth_password=None, html_message=html_message  # send_mail function
                          )

                messages.info(request,
                              'Konto o nazwie: {}, zostało utworzone, zaloguj się!'.format(username),
                              extra_tags="info"
                              )
                return HttpResponseRedirect('/sklep/logowanie/in/')

            else:
                messages.error(request, 'Wprowadzone zostały niepoprawne dane, hasła nie zgadzają się, lub konto o '
                                        'podanych parametrach juz istnieje. Pamiętej! Hasło musi zawierać przynajmniej '
                                        '8 znaków, w tym (przynajmniej) jeden znak specjalny lub cyfrę',
                               extra_tags="error")
                return HttpResponseRedirect('/sklep/rejestracja/in/')

        elif 'login' in self.request.POST:
            login_form = UserLogin(self.request.POST or None)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/sklep/')
                else:
                    messages.info(request, 'Błędny login lub hasło ', extra_tags="info")
                    return HttpResponseRedirect('/sklep/logowanie/in/')

        form = SearchForm()
        user_form = UserForms()
        email_form = EmailShop()
        login_form = UserLogin()
        context = {
            'form': form,
            'user_form': user_form,
            'email_form': email_form,
            'login_form': login_form,
            'shop_products': queryset,
            'shop_products_cart': len(queryset_cart),
            'shop_products_cart_list': queryset_cart,
            'order': order,
            'shopping_address_pk': shopping_address_pk,
            'category': category,
        }
        return render(self.request, 'shop/shop_search.html', context)

class ShopGetView():#all get class
    def get(self,request, slug=None,  *args, **kwargs):
        form = SearchForm()
        pay_form = PaymentForms()
        user_form = UserForms()
        email_form = EmailShop()
        login_form = UserLogin()

        queryset = Product.objects.all()
        queryset_cart_all_users = OrderItem.objects.all()
        Customer.objects.get_or_create(device='is_anonymous')
        category = Category.objects.all()
        order = ''
        customer = ''
        shopping_address_pk = 0
        try:
            if request.user.is_authenticated:
                customer, created = Customer.objects.get_or_create(user=request.user)
                try:
                    shopp_add_pk, create = ShoppingAddress.objects.get_or_create(
                                                                                customer=customer,
                                                                                email=request.user.email
                                                                                )
                except:
                    shopp_add_pk, create = ShoppingAddress.objects.get_or_create(customer=customer)
                shopping_address_pk = shopp_add_pk.pk
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
            'email_form': email_form,
            'login_form': login_form,
            'shop_products': queryset,
            'shop_products_cart': len(queryset_cart),
            'shop_products_cart_list': queryset_cart,
            'order': order,
            'customer': customer,
            'shopping_address_pk': shopping_address_pk,
            'category': category,
        }
        if slug is not None:
            context['slug'] = slug

        return render(self.request, self.template_name, context)



# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Class area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Template/Search area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


class ShopAllListView(ShopGetView, ShopPostView, View):                              # All products from shop
    template_name = 'shop/shop.html'

class ShopProductDetailView(ShopPostView, View):                       # Detail products from shop
    template_name = 'shop/shop_detail.html'

    def get(self, request, pk=None, *args, **kwargs):
        form = SearchForm()
        queryset_cart_all_users = OrderItem.objects.all()
        category = Category.objects.all()
        shopping_address_pk = 0
        try:
            if request.user.is_authenticated:
                customer, created = Customer.objects.get_or_create(user=request.user)
                shopp_add_pk, create = ShoppingAddress.objects.get_or_create(customer=customer)
                shopping_address_pk = shopp_add_pk.pk
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
            'shopping_address_pk': shopping_address_pk,
            'category': category,
        }
        if pk is not None:
            object = get_object_or_404(Product, pk=pk)
            context['object'] = object

        return render(request, self.template_name, context)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Template/Search area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Shopping cart area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class ShopCartView(ShopGetView, ShopPostView, View):
    template_name = 'shop/shop_cart.html'

class ShopCartViewDetail(ShopGetView, ShopPostView, View):
    template_name = 'shop/shop_cart.html'

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Shopping cart area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Payment area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class ShopPaymentView(ShopGetView, ShopPostView, View):
    template_name = 'shop/payment/shop_payment.html'

class ShopPayPalView(ShopGetView, View):
    template_name = 'shop/payment/shop_paypal.html'

class ShopPayPalEndView(View):
    template_name = 'shop/payment/shop_paypal_end.html'
    def get(self,request, pk=None,  *args, **kwargs):
        Customer.objects.get_or_create(device='is_anonymous')
        order = ''

        try:
            if request.user.is_authenticated:
                user_customer = request.user
                customer, created = Customer.objects.get_or_create(user=user_customer)
            else:
                device = request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        except:
            pass
        order.complete = True
        order.save()
        try:
            shopping_address = ShoppingAddress.objects.get(customer=customer, order=order)
            order_items = OrderItem.objects.all()
            subject = 'Potwierdzenie zakupu produktów, ridelectric.pl'  # subject of email
            message = 'Dziękujemy za dokonanie zakupów naszych produktów ridelectric.pl'  # reserve messego
            from_email = settings.EMAIL_HOST_USER  # adres from send and details from settings
            recipient_list = [shopping_address.email, from_email]  # delivery email
            html_message = loader.render_to_string('shop/payment/email_shop_confirmation.html',
                                                   {
                                                       'order_items': order_items,
                                                       'order': order,
                                                       'shopping_id': shopping_address.order.id,
                                                       'first_name': shopping_address.first_name.capitalize(),
                                                       'last_name': shopping_address.last_name.capitalize(),
                                                       'street_name': shopping_address.street_name.capitalize(),
                                                       'street_number': shopping_address.street_number,
                                                       'city': shopping_address.city.capitalize(),
                                                       'zip_code': shopping_address.zip_code
                                                   }
                                                )
            send_mail(subject, message, from_email, recipient_list, fail_silently=True, auth_user=None,
                      auth_password=None, html_message=html_message                     # send_mail function
                      )
        except:
            pass
        order.complete = True
        order.save()
        return render(self.request, self.template_name )

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Payment area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Login area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class ShopLoginView(ShopGetView, ShopPostView, View):
    template_name = 'shop/login/shop_login.html'

class ShopRegisterView(ShopGetView, ShopPostView, View):
    template_name = 'shop/login/shop_register.html'

class ShopUserView(ShopGetView, ShopPostView, View):
    template_name = 'shop/login/shop_user.html'

class ShopLogoutView(ShopPostView, View):
    def get(self, request, pk=None, *args, **kwargs):
        logout(request)
        messages.info(request, 'Poprawnie wylogowano', extra_tags="info")
        return HttpResponseRedirect('/sklep/logowanie/in/')

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End Login area >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>