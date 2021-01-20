from django.urls import path
from django.contrib.auth import views as auth_views
from shop.views import *


app_name = 'shop'
urlpatterns = [
    path('sklep/', ShopAllListView.as_view(), name='sklep'),
    path('sklep/<str:slug>/', ShopAllListView.as_view(template_name = 'shop/shop_EV.html'), name='sklep_EV_1'),
    path('sklep/produkty/<int:pk>/', ShopProductDetailView.as_view(), name='product'),
    path('sklep/koszyk/produkty/', ShopCartView.as_view(), name='cart'),
    path('sklep/koszyk/produkty/<int:pk>/', ShopCartViewDetail.as_view(), name='cart_delete'),
    path('sklep/koszyk/zaplac/', ShopPaymentView.as_view(), name='payment'),
    path('sklep/koszyk/zaplac/paypal/', ShopPayPalView.as_view(), name='paypal'),
    path('sklep/koszyk/zaplac/paypal/end/', ShopPayPalEndView.as_view(), name='paypalend'),
    path('sklep/logowanie/in/', ShopLoginView.as_view(), name='login'),
    path('sklep/rejestracja/in/', ShopRegisterView.as_view(), name='register'),
    path('sklep/user/', ShopUserView.as_view(), name='user'),
    path('sklep/wyloguj/out/', ShopLogoutView.as_view(), name='logoff'),
    path('sklep/logowanie/resethasla/',
         auth_views.PasswordResetView.as_view(
                                              template_name="shop/login/shop_reset_password.html",
                                              email_template_name='shop/login/shop_password_reset_email.html',
                                              subject_template_name="shop/login/shop_password_reset_subject.txt"
                                              ),
         name='password_reset'
         )
    ]
