from django.urls import path, include
from .views import ShoppingaddressAPIView, OrderItemAPIView, OrderAPIView

urlpatterns = [
    path('api/<int:pk>/', ShoppingaddressAPIView.as_view({'get': 'list', 'post': 'update',}), name='api-detail'),
    path('api/orders/', OrderAPIView.as_view({'get': 'list'}), name='orders'),
    path('api/orders/<int:pk>/', OrderItemAPIView.as_view({'get': 'list',}), name='orders-itemorders'),
]
