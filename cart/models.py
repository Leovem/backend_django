from django.db import models
from authapp.models import Usuario
from productsCart.models import Producto

class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usuario_id')  # o ForeignKey si usas modelo de usuario
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carritos'

class CarritoItem(models.Model):
    id = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, db_column='carrito_id')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='producto_id')  # o ForeignKey si tienes el modelo Producto
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'carrito_items'
