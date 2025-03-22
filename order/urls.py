from django.urls import path, include
from django.contrib import admin
from rest_framework import routers # type: ignore

from order import viewsets

router = routers.SimpleRouter()
router.register(r'orders', viewsets.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('orders/', include('order.urls')),
    path('products/', include('product.urls')),
]