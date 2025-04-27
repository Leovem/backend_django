from django.db import models

class InteraccionProducto(models.Model):
    usuario_id = models.IntegerField()
    producto_id = models.IntegerField()
    tipo_interaccion = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'interacciones_producto'