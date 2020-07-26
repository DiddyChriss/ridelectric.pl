from django.test import TestCase
from django.urls import reverse, resolve
from shop.views import shop


class TestUrls(TestCase):

    def test_shop_url(self):
        url = reverse('sklep')
        self.assertEquals(resolve(url).func, shop)

