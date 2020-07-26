from django.urls import path
from shop.views import shop, shop_test, shop_test_slug

app_name = 'shop'
urlpatterns = [
    path('sklep/', shop, name='sklep'),
    path('shop/', shop_test, name='shop_test'),
    path('shop/<slug:slug>/', shop_test_slug, name='shop_test_slug')
]