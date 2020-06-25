from django.test import TestCase, Client
from django.urls import reverse
from home.views import home, contact, polityka_prywatnosci, regulamin
from home.models import Contact_models

class TestModels (TestCase):

    def setUp(self):
        self.contact_data = Contact_models.objects.create(
            name='Diddy',
            surname='Chriss',
            company='beExcellent',
            email='DiddyChriss@gmail.com',
            question='test question'
        )

    def test_models(self):
        self.assertEquals(self.contact_data.name, 'Diddy')

