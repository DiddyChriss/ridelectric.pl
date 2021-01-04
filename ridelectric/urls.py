"""ridelectric URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('home.urls', namespace='home')),
    path('', include('shop.urls', namespace='shop')),
    path('sklep/', include('shop.api.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('sklep/logowanie/resethasla/wyslane/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="shop/login/shop_reset_password_send.html"
            ),
            name='password_reset_done'
        ),
    path('password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="shop/login/shop_reset_password_confirm.html"
            ),
            name='password_reset_confirm'
        ),
    path('sklep/logowanie/resethasla/zaloguj/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="shop/login/shop_reset_password_done.html"
            ),
            name='password_reset_complete'
        ),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)