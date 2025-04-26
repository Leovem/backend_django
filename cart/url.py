from django.urls import path
from .views import agregar_producto_al_carrito, obtener_carrito_usuario, eliminar_producto_del_carrito

urlpatterns = [
    path('agregar-producto/', agregar_producto_al_carrito, name='agregar-producto-al-carrito'),
    path('<int:usuario_id>/', obtener_carrito_usuario, name='obtener_carrito_usuario'),
    path('eliminar-del-carrito/', eliminar_producto_del_carrito, name='eliminar_producto_del_carrito'),

]
