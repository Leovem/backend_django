from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InteraccionProducto

class RegistrarInteraccionView(APIView):
    def post(self, request):
        try:
            usuario_id = request.data.get('usuario_id')
            producto_id = request.data.get('producto_id')
            tipo_interaccion = request.data.get('tipo_interaccion')

            # Validación simple (puedes mejorarla luego)
            if not usuario_id or not producto_id or not tipo_interaccion:
                return Response({'error': 'Faltan campos obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

            # Guardar en la base de datos
            interaccion = InteraccionProducto.objects.create(
                usuario_id=usuario_id,
                producto_id=producto_id,
                tipo_interaccion=tipo_interaccion
            )

            return Response({'mensaje': 'Interacción registrada correctamente'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("ERROR EN VISTA:", str(e))  # Mostrar en la consola
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
