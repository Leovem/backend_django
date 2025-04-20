from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Carrito, CarritoItem
from productsCart.models import Producto
from django.shortcuts import get_object_or_404
from authapp.models import Usuario  # Asegúrate de importar el modelo Usuario

@api_view(['POST'])
def agregar_producto_al_carrito(request):
    # Obtener el ID del usuario y el ID del producto desde la solicitud
    usuario_id = request.data.get('usuario_id')
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad', 1)  # La cantidad por defecto es 1 si no se especifica

    # Verificar que los datos necesarios existan
    if not usuario_id or not producto_id:
        return Response({'detail': 'Faltan datos necesarios'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Obtener el usuario
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Obtener el producto
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({'detail': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    # Buscar el carrito del usuario, si no existe, crear uno nuevo
    carrito, created = Carrito.objects.get_or_create(usuario=usuario)

    # Verificar si el producto ya está en el carrito
    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    # Si el producto ya está en el carrito, solo actualizamos la cantidad
    if not created:
        carrito_item.cantidad += cantidad
        carrito_item.save()
    else:
        # Si es un producto nuevo en el carrito, se establece la cantidad inicial
        carrito_item.cantidad = cantidad
        carrito_item.save()

    # Responder con el carrito actualizado
    return Response({
        'carrito_id': carrito.id,
        'producto_id': producto.id,
        'cantidad': carrito_item.cantidad,
    }, status=status.HTTP_201_CREATED)
