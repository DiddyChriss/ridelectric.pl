from django.urls import path
from shop.views import (
    ShopAllListView,
    Shop_Product_DetailView,
    Shop_Cart_View
    )

app_name = 'shop'
urlpatterns = [
    path('sklep/', ShopAllListView.as_view(), name='sklep'),
    path('sklep/EV/', ShopAllListView.as_view(template_name = 'shop/EV/shop_EV.html'), name='sklep_EV_1'),
    path('sklep/EV7/', ShopAllListView.as_view(template_name = 'shop/EV/shop_EV_7kW.html') , name='sklep_EV_2'),
    path('sklep/EV22/', ShopAllListView.as_view(template_name = 'shop/EV/shop_EV_22kW.html') , name='sklep_EV_22'),
    path('sklep/EVcable/', ShopAllListView.as_view(template_name = 'shop/EV/shop_EV_cable.html') , name='sklep_cable'),
    path('sklep/PV/', ShopAllListView.as_view(template_name = 'shop/PV/shop_PV.html'), name='sklep_PV'),
    path(
        'sklep/PVmoduly/',
        ShopAllListView.as_view(template_name = 'shop/PV/shop_PVmodules.html'),
        name='sklep_modules'
        ) ,
    path(
        'sklep/PVinwertery/',
        ShopAllListView.as_view(template_name = 'shop/PV/shop_PVinverters.html'),
        name='sklep_inverters'
        ) ,
    path(
        'sklep/PVpozostale/',
        ShopAllListView.as_view(template_name = 'shop/PV/shop_PVothers.html'),
        name='sklep_others'
        ) ,
    path('sklep/produkty/<int:pk>/', Shop_Product_DetailView.as_view(), name='product'),
    path('sklep/koszyk/', Shop_Cart_View.as_view(), name='cart'),
    path('sklep/koszyk/<int:pk>/', Shop_Cart_View.as_view(), name='cart_delete')

]
