from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password

class RegistroView(APIView):
    def post(self, request):
        data = request.data
        data['password'] = make_password(data['password'])  # encriptar
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario registrado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = Usuario.objects.get(email=email)
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "mensaje": "Inicio de sesión exitoso",
                    "id": user.id,
                    "nombre": user.nombre_completo,
                    "Token refresh": str(refresh),
                    "Token access": str(refresh.access_token)
                })
            else:
                return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class EditarUsuarioView(APIView):
    def put(self, request, id):
        usuario = get_object_or_404(Usuario, id=id)
        data = request.data

        if 'password' in data:
            data['password'] = make_password(data['password'])  # encriptar si se actualiza

        serializer = UsuarioSerializer(usuario, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario actualizado con éxito"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)