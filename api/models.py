from django.db import models


# modelo de tipo producto
class TipoProducto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tipo_producto'


# modelo de productos
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to='images/images/', blank=True, null=True)
    stock = models.IntegerField()
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    precioOferta = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "producto"

# modelo tipo de usuario


class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tipo_usuario'

# modelo usuario


class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    suscrito = models.BooleanField(default=False)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "usuario"


# Modelo de pais
class Pais(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'pais'

# Modelo de ciudad


class Ciudad(models.Model):
    nombre = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'ciudad'


class Venta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    direccion = models.CharField(max_length=200)
    Tarjeta = models.CharField(max_length=50)
    Ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.nombre

    class Meta:
        db_table = "venta"


class ProductoVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.producto.nombre

    class Meta:
        db_table = "producto_venta"
