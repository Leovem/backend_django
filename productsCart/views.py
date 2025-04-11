from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto

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
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio
            } for producto in productos]
            return Response(productos_data, status=status.HTTP_200_OK)
        except Exception as e:
            print("ERROR EN VISTA:", str(e))  # Mostrar en la consola
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
