from django.db import models
from django.urls import reverse


class Shop_models(models.Model):                  #creating of data in models
    name_shop        = models.CharField(max_length=200)
    date_shop        = models.DateTimeField(auto_now=True)
    coment_shop      = models.TextField()
    confirmation_buy = models.BooleanField(null=True)
    price            = models.DecimalField(decimal_places=2, max_digits=500, default=True)

    def __str__(self, *args, **kwargs):
        return (self.name_shop)            #show database form models as a name not "search object (id=nr)"

    def get_absolute_url(self):
        return reverse("shop:shop_test_slug", kwargs={'slug': self.name_shop})
        #return f"/shop/{self.name_shop}/"


