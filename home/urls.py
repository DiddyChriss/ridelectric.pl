from django.urls import path
from home.views import home, polityka_prywatnosci, regulamin, ContactView

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('polityka_prywatnosci/', polityka_prywatnosci, name='polityka_prywatnosci'),
    path('regulamin/', regulamin, name='regulamin')
]