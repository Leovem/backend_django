from django.urls import path
from .views import CatalogoProductosView, ObtenerProductosPorCategoriaView

urlpatterns = [
    path('catalogo/', CatalogoProductosView.as_view(), name='catalogo_productos'),
    path('categoria/<int:categoria_id>/', ObtenerProductosPorCategoriaView.as_view(), name='obtener_productos_por_categoria'),
]
