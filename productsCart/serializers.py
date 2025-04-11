from rest_framework import serializers
from .models import Producto, Categoria, CaracteristicasProducto

# Serializer para Características de Producto
class CaracteristicasProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaracteristicasProducto
        fields = ['nombre', 'valor']

# Serializer para Categoría
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

# Serializer para Producto
class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()  # Relación con la categoría
    caracteristicas = CaracteristicasProductoSerializer(many=True)  # Relación con las características

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen_url', 'caracteristicas']
