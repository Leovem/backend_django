from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Pedido, PedidoDetalle, Envio, MetodoPago, Pago
from authapp.models import Usuario
from productsCart.models import Producto
from cart.models import Carrito, CarritoItem
from datetime import timedelta
from django.utils import timezone

@api_view(['POST'])
def compra_directa(request):
    usuario_id = request.data.get('usuario_id')
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad', 1)
    metodo_pago_id = request.data.get('metodo_pago_id')
    direccion_envio = request.data.get('direccion_envio')
    tipo_entrega = request.data.get('tipo_entrega', 'estándar')

    if not usuario_id or not producto_id or not metodo_pago_id or not direccion_envio:
        return Response({'detail': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario = Usuario.objects.get(id=usuario_id)
        producto = Producto.objects.get(id=producto_id)
        metodo_pago = MetodoPago.objects.get(id=metodo_pago_id)
    except Usuario.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Producto.DoesNotExist:
        return Response({'detail': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except MetodoPago.DoesNotExist:
        return Response({'detail': 'Método de pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    precio_unitario = producto.precio
    total = precio_unitario * cantidad

    pedido = Pedido.objects.create(
        usuario=usuario,
        estado='pendiente',
        total=total
    )

    PedidoDetalle.objects.create(
        pedido=pedido,
        producto=producto,
        cantidad=cantidad,
        precio_unitario=precio_unitario
    )

    pago = Pago.objects.create(
        pedido=pedido,
        metodo_pago=metodo_pago,
        estado='pendiente',
        monto=total
    )

    fecha_entrega_estimada = timezone.now() + timedelta(days=3)

    envio = Envio.objects.create(
        pedido=pedido,
        direccion_envio=direccion_envio,
        tipo_entrega=tipo_entrega,
        estado_envio='pendiente',
        fecha_entrega_estimada=fecha_entrega_estimada
    )

    return Response({
        'pedido_id': pedido.id,
        'producto': producto.nombre,
        'cantidad': cantidad,
        'total': total,
        'pago_id': pago.id,
        'metodo_pago': metodo_pago.tipo,
        'estado_pago': pago.estado,
        'envio_id': envio.id,
        'direccion_envio': envio.direccion_envio,
        'fecha_estimada_entrega': envio.fecha_entrega_estimada
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def confirmar_pago(request):
    pago_id = request.data.get('pago_id')

    if not pago_id:
        return Response({'detail': 'Falta el ID del pago'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({'detail': 'Pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Cambiar estado del pago
    pago.estado = 'pagado'
    pago.save()

    # Cambiar estado del pedido relacionado
    pedido = pago.pedido
    pedido.estado = 'procesado'
    pedido.save()

    return Response({
        'mensaje': 'Pago confirmado y pedido procesado',
        'pedido_id': pedido.id,
        'estado_pedido': pedido.estado,
        'estado_pago': pago.estado
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def comprar_carrito(request):
    usuario_id = request.data.get('usuario_id')
    metodo_pago_id = request.data.get('metodo_pago_id')
    direccion_envio = request.data.get('direccion_envio')
    tipo_entrega = request.data.get('tipo_entrega', 'estándar')

    if not usuario_id or not metodo_pago_id or not direccion_envio:
        return Response({'detail': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario = Usuario.objects.get(id=usuario_id)
        metodo_pago = MetodoPago.objects.get(id=metodo_pago_id)
        carrito = Carrito.objects.get(usuario=usuario)
        items = CarritoItem.objects.filter(carrito=carrito)
    except Usuario.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except MetodoPago.DoesNotExist:
        return Response({'detail': 'Método de pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Carrito.DoesNotExist:
        return Response({'detail': 'Carrito no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if not items:
        return Response({'detail': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)

    total = 0
    for item in items:
        total += item.producto.precio * item.cantidad

    pedido = Pedido.objects.create(
        usuario=usuario,
        estado='pendiente',
        total=total
    )

    for item in items:
        PedidoDetalle.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )

        # Descontar del stock
        item.producto.stock -= item.cantidad
        item.producto.save()

    pago = Pago.objects.create(
        pedido=pedido,
        metodo_pago=metodo_pago,
        estado='pendiente',
        monto=total
    )

    fecha_entrega_estimada = timezone.now() + timedelta(days=3)

    envio = Envio.objects.create(
        pedido=pedido,
        direccion_envio=direccion_envio,
        tipo_entrega=tipo_entrega,
        estado_envio='pendiente',
        fecha_entrega_estimada=fecha_entrega_estimada
    )

    # Limpiar el carrito del usuario
    items.delete()

    return Response({
        'pedido_id': pedido.id,
        'total': total,
        'estado_pedido': pedido.estado,
        'pago_id': pago.id,
        'estado_pago': pago.estado,
        'metodo_pago': metodo_pago.tipo,
        'envio_id': envio.id,
        'direccion_envio': envio.direccion_envio,
        'fecha_estimada_entrega': envio.fecha_entrega_estimada
    }, status=status.HTTP_201_CREATED)