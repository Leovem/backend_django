from django.urls import path
from .views import agregar_producto_al_carrito

urlpatterns = [
    path('agregar-producto/', agregar_producto_al_carrito, name='agregar-producto-al-carrito'),
]
