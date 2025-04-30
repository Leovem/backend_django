from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from rest_framework.exceptions import NotFound

#class CatalogoProductosView(APIView):
#    def get(self, request):
#        productos = Producto.objects.all()  # Obtiene todos los productos de la tabla 'productos'
#        productos_data = [{"nombre": producto.nombre, "descripcion": producto.descripcion, "precio": producto.precio} for producto in productos]
#        return Response(productos_data, status=status.HTTP_200_OK)


class CatalogoProductosView(APIView):
    def get(self, request):
        try:
            productos = Producto.objects.all()
            productos_data = [{
                "id": producto.id,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "stock" : producto.stock,
                "imagen_url": producto.imagen_url
            } for producto in productos]
            return Response(productos_data, status=status.HTTP_200_OK)
        except Exception as e:
            print("ERROR EN VISTA:", str(e))  # Mostrar en la consola
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ObtenerProductosPorCategoriaView(APIView):
    def get(self, request, categoria_id):
        try:
            # Filtrar productos por categoría
            productos = Producto.objects.filter(categoria_id=categoria_id)
            
            # Verificar si hay productos para esta categoría
            if not productos.exists():
                return Response({'detail': 'No se encontraron productos para esta categoría'}, status=status.HTTP_404_NOT_FOUND)

            # Serializar los productos encontrados
            productos_data = [{
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'stock': producto.stock,
                'imagen_url': producto.imagen_url,
                'categoria': producto.categoria.nombre,  # Agregamos el nombre de la categoría
            } for producto in productos]

            return Response(productos_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Manejo de errores
            print("ERROR EN VISTA:", str(e))
            return Response({"error": "Error al obtener los productos por categoría"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)