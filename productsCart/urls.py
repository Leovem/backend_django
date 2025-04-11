from django.urls import path
from .views import CatalogoProductosView

urlpatterns = [
    path('catalogo/', CatalogoProductosView.as_view(), name='catalogo_productos'),
]
