from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'categorias'  # Usamos la tabla 'categorias' en la base de datos existente

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    # Cambia estos 👇
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE)

    imagen_url = models.TextField()

    class Meta:
        db_table = 'productos'


class CaracteristicaProducto(models.Model):
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con la tabla 'productos'
    nombre = models.CharField(max_length=100)
    valor = models.TextField()

    class Meta:
        db_table = 'caracteristicas_producto'  # Usamos la tabla 'caracteristicas_producto' en la base de datos existente


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    direccion = models.TextField()

    class Meta:
        db_table = 'sucursales'  # Usamos la tabla 'sucursales' en la base de datos existente
