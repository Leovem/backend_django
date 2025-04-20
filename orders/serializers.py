from rest_framework import serializers
from .models import Pedido, PedidoDetalle
from productsCart.models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio']

class PedidoDetalleSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = PedidoDetalle
        fields = ['producto', 'cantidad', 'precio_unitario']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = PedidoDetalleSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'fecha', 'estado', 'total', 'detalles']
