from django.test import TestCase, Client
from django.urls import reverse
from home.views import home, contact, polityka_prywatnosci, regulamin
from home.models import Contact_models

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('contact')
        self.contact_data = Contact_models.objects.create(
            name='Diddy',
            surname='Chriss',
            company='beExcellent',
            email='DiddyChriss@gmail.com',
            question='test question'
        )

    def test_post_contact_views(self):

        response = self.client.post(self.contact_url, {
            'name' : 'Diddy',
            'surname' : 'Chriss',
            'company' : 'beExcellent',
            'email' : 'DiddyChriss@gmail.com',
            'question': 'test question'
        })

        self.assertTrue(response, True)

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'contact.html')

    









