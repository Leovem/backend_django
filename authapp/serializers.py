from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre_completo', 'email', 'password', 'telefono', 'direccion', 'fecha_registro', 'rol_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return Usuario.objects.create(**validated_data)
