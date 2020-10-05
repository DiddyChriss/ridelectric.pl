from django.db import models
from django.urls import reverse


class shop_products(models.Model):             #creating of data in models
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
    date_product             = models.DateTimeField(auto_now=True)
    description_product      = models.TextField()
    confirmation_buy         = models.BooleanField(null=True)
    price_product            = models.DecimalField(decimal_places=2, max_digits=20, default=True)
    image_product            = models.FileField(upload_to='upload/', null=True)

    def __str__(self, *args, **kwargs):
        return (self.title_product)            #show database form models as a name not "search object (id=nr)"

    def get_absolute_url(self, **kwargs):
        return reverse("shop:product", kwargs={
            'pk' : self.pk

        }
                       )

class shop_products_cart(models.Model):             #creating of data in models

    title_cart            = models.CharField(max_length=40, null=True)
    date_cart             = models.DateTimeField(auto_now=True)
    description_cart      = models.TextField()
    price_cart            = models.DecimalField(decimal_places=2, max_digits=20, default=True)
    image_cart            = models.FileField(upload_to='upload/cart/', null=True)



    def __str__(self, *args, **kwargs):
        return (self.title_cart)            #show database form models as a name not "search object (id=nr)"

    # def get_absolute_url(self, **kwargs):
    #     return reverse("shop:product", kwargs={
    #         'pk' : self.pk
    #
    #     }
    #                    )


