from django.db import models
from authapp.models import Usuario
from productsCart.models import Producto

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pedidos'  # ← Nombre exacto de la tabla en la base de datos

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pedido_detalles'

class MetodoPago(models.Model):
    tipo = models.CharField(max_length=50)

    class Meta:
        db_table = 'metodos_pago'

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    paypal_payment_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'pagos'

class Envio(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    direccion_envio = models.TextField()
    tipo_entrega = models.CharField(max_length=50)
    estado_envio = models.CharField(max_length=50, default='pendiente')
    fecha_envio = models.DateTimeField(null=True, blank=True)
    fecha_entrega_estimada = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'envios'
