from django.test import TestCase
from django.urls import reverse, resolve
from home.views import home, contact, polityka_prywatnosci, regulamin

class TestUrls(TestCase):

    def test_home_url(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_contact_url(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)

    def test_polityka_prywatnosci_url(self):
        url = reverse('polityka_prywatnosci')
        self.assertEquals(resolve(url).func, polityka_prywatnosci)

    def test_regulamin_url(self):
        url = reverse('regulamin')
        self.assertEquals(resolve(url).func, regulamin)

