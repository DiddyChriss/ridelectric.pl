from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=20, null=True)
    device = models.CharField(max_length=200, null=True)
    confirm = models.BooleanField(null=True)

    def __str__(self):
        if self.name is None:
            name = self.device
        else:
            name= self.name
        return name

class Product(models.Model):
    EV7KW = 'E7'
    EV22KW = 'E2'
    EVCABLE = 'EC'
    PVMODULES = 'PM'
    PVINVERTERS = 'PI'
    PVOTHERS = 'PO'

    shop_categories = [
        (EV7KW, 'EV_7KW'),
        (EV22KW, 'EV_22KW'),
        (EVCABLE, 'EV_CABLE'),
        (PVMODULES, 'PV_MODULES'),
        (PVINVERTERS, 'PV_INVERTERS'),
        (PVOTHERS, 'PV_OTHERS'),
    ]
    categories_product = models.CharField(
        max_length=2,
        choices=shop_categories,
        default=EV7KW,
    )
    title_product            = models.CharField(max_length=40, null=True)
    description_product      = models.TextField()
    price_product            = models.DecimalField(decimal_places=2, max_digits=20, default=True)
    image_product            = models.FileField(upload_to='upload/', null=True)

    def __str__(self, *args, **kwargs):
        return (self.title_product)

    def get_absolute_url(self, **kwargs):
        return reverse("shop:product", kwargs={
            'pk' : self.pk

        }
                       )

    def get_image(self):
        try:
            url = self.image_product.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self, *args, **kwargs):
        return  str(self.id)

    @property
    def get_all_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total_price for item in orderitems])
        return total

    @property
    def get_vat_price(self):
        total = float(self.get_all_price) * float(1.23)
        return total

    def vat(self):
        total = float(self.get_vat_price) - float(self.get_all_price)
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self, *args, **kwargs):
        return str('order: {}, name: {},'.format(self.order, self.product.title_product))

    @property
    def get_total_price(self):
        total= self.product.price_product * self.quantity
        return total

class ShoppingAddress(models.Model):
    customer            = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order               = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    firstname           = models.CharField(max_length=200, null=True)
    lastname            = models.CharField(max_length=200, null=True)
    email               = models.EmailField(max_length=200, null=True)
    number              = models.CharField(max_length=200, null=True)
    streetnumber        = models.CharField(max_length=200, null=True)
    city                = models.CharField(max_length=200, null=True)
    zipcode             = models.CharField(max_length=200, null=True)
    comment             = models.CharField(max_length=200, null=True)
    date_added          = models.DateTimeField(auto_now_add=True)


    def __str__(self, *args, **kwargs):
            return str('{} ,order: {}, name: {},'.format(self.id,self.order, self.firstname))
