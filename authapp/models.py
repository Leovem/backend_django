from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.TextField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    rol_id = models.IntegerField(blank=True, null=True)  # O FK si quieres más adelante

    class Meta: 
        db_table = 'usuarios'
