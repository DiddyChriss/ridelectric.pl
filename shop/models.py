from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    name = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True, unique=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    confirm = models.BooleanField(null=True)

    class Meta:
        verbose_name_plural = "1. Customer"

    def __str__(self):
        return str('{}, {},'.format(self.user, self.device))

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    category = TreeForeignKey(
                              'self',
                              on_delete=models.CASCADE,
                              null=True, blank=True,
                              related_name='children'
                              )
    class Meta:
        verbose_name_plural = "2. Category"

    class MPTTMeta:
        parent_attr = 'category'
        order_insertion_by=['name']

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    title_product = models.CharField(max_length=40, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True) # models.ManyToManyField(Category)
    description_product = models.TextField(null=True)
    description_product_2 = models.CharField(max_length=60, null=True, blank=True, default=None)
    price_product = models.DecimalField(decimal_places=2, max_digits=20, default=True)
    image_product = models.FileField(upload_to='upload/', null=True)
    image_product_1 = models.FileField(upload_to='upload/', null=True, blank=True)
    image_product_2 = models.FileField(upload_to='upload/', null=True, blank=True)
    image_product_3 = models.FileField(upload_to='upload/', null=True, blank=True)
    image_product_4 = models.FileField(upload_to='upload/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "3. Product"

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

    class Meta:
        verbose_name_plural = "4. Order"

    def __str__(self, *args, **kwargs):
        return  str('{}, {}'.format(self.id, self.customer))

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

    class Meta:
        verbose_name_plural = "5. OrderItem"

    def __str__(self, *args, **kwargs):
        return str('order: {}, name: {},'.format(self.order, self.product.title_product))

    @property
    def get_total_price(self):
        total= self.product.price_product * self.quantity
        return total

class ShoppingAddress(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, blank=True, null=True, unique=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    street_name = models.CharField(max_length=200, null=True)
    street_number = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)
    comment = models.TextField(max_length=300, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "6. ShoppingAddress"

    def __str__(self, *args, **kwargs):
            return str('{}, {}'.format(self.pk, self.customer))
