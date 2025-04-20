from django.urls import path
from .views import compra_directa, confirmar_pago

urlpatterns = [
    path('compra-directa/', compra_directa, name='compra-directa'),
    path('confirmar-pago/', confirmar_pago),
]
