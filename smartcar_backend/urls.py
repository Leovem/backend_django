from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.urls')),
    path('api/products/', include('productsCart.urls')),
    path('api/cart/', include('cart.url')),
    path('api/orders/', include('orders.url')),
    path('api/payment/', include('payment.url')),
]
