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

@api_view(['GET'])
def obtener_carrito_usuario(request, usuario_id):
    # Verificamos que el usuario exista
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Intentamos obtener el carrito del usuario
    try:
        carrito = Carrito.objects.get(usuario=usuario)
    except Carrito.DoesNotExist:
        return Response({'detail': 'El usuario no tiene un carrito'}, status=status.HTTP_404_NOT_FOUND)

    # Obtenemos todos los ítems del carrito
    items = CarritoItem.objects.filter(carrito=carrito)

    # Serializamos manualmente los datos (puedes usar un serializer si tienes)
    productos_en_carrito = []
    for item in items:
        productos_en_carrito.append({
            'producto_id': item.producto.id,
            'nombre': item.producto.nombre,
            'imagen_url': item.producto.imagen_url,
            'precio': item.producto.precio,
            'cantidad': item.cantidad
        })

    return Response({
        'carrito_id': carrito.id,
        'usuario_id': usuario.id,
        'productos': productos_en_carrito
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def eliminar_producto_del_carrito(request):
    usuario_id = request.data.get('usuario_id')
    producto_id = request.data.get('producto_id')

    # Validación de datos
    if not usuario_id or not producto_id:
        return Response({'detail': 'Faltan datos necesarios'}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener el usuario
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Obtener el carrito del usuario
    try:
        carrito = Carrito.objects.get(usuario=usuario)
    except Carrito.DoesNotExist:
        return Response({'detail': 'El carrito no existe'}, status=status.HTTP_404_NOT_FOUND)

    # Buscar el item del producto dentro del carrito
    try:
        carrito_item = CarritoItem.objects.get(carrito=carrito, producto__id=producto_id)
        carrito_item.delete()
        return Response({'detail': 'Producto eliminado del carrito'}, status=status.HTTP_200_OK)
    except CarritoItem.DoesNotExist:
        return Response({'detail': 'Producto no encontrado en el carrito'}, status=status.HTTP_404_NOT_FOUND)
