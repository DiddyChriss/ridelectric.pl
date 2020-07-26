from django.urls import path
from home.views import home, contact, polityka_prywatnosci, regulamin

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('polityka_prywatnosci/', polityka_prywatnosci, name='polityka_prywatnosci'),
    path('regulamin/', regulamin, name='regulamin')
]