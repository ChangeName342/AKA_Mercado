from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class Clientes(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    fono = models.CharField(max_length=10, null=True)
    email = models.EmailField()
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=45, default='Cliente', editable=False)

class Pedidos(models.Model):
    OPCIONES_ESTADO = (
        ('Entregado', 'ENTREGADO'),
        ('En camino', 'EN CAMINO')
    )
    ENTREGA = (
        ('Domicilio', 'DOMICILIO'),
        ('Retiro en Tienda', 'RETIRO EN TIENDA')
    )
    idPedido = models.AutoField(primary_key = True)
    fecha = models.DateField()
    estado = models.CharField(max_length=45, choices=OPCIONES_ESTADO)
    tipo_entrega = models.CharField(max_length=45, choices=ENTREGA)
    precio = models.IntegerField()
    Clientes_rut = models.ForeignKey(Clientes, on_delete=models.CASCADE)

    def calcular_total(self):
        productos_pedido = Productos_has_Pedidos.objects.filter(Pedidos_id=self)
        total = sum(producto.Productos_id.precio for producto in productos_pedido)
        return total

    def obtener_resumen_productos(self):
        productos_pedido = Productos_has_Pedidos.objects.filter(Pedidos_id=self)
        resumen = [
            {
                'producto': producto.Productos_id.nombre,
                'precio': producto.Productos_id.precio,
                'cantidad': producto.Productos_id.cantidad
            }
            for producto in productos_pedido
        ]
        return resumen

class MetodoPago(models.Model):
    titular = models.CharField(max_length=150)
    ccv = models.IntegerField()
    fecha_vencimiento = models.DateField()
    direccion = models.TextField()
    Clientes_rut = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    Pedidos_id = models.ForeignKey(Pedidos, on_delete=models.CASCADE)

class Productos(models.Model):
    OPCIONES_CATEGORIA = (
        ('Rotisería', 'ROTISERÍA'),
        ('Bebidas y Abarrotes', 'BEBIDAS Y ABARROTES'),
        ('Carnes', 'CARNES')
    )
    idProd = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length=150)
    precio = models.IntegerField()
    imagen = models.ImageField(null=True)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    categoria = models.CharField(max_length=60, choices=OPCIONES_CATEGORIA, null=True)

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'

class Administradores(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    contraseña = models.CharField(max_length=255)
    email = models.EmailField()
    rol = models.CharField(max_length=45, default='Administrador', editable=False)  

class Productos_has_Pedidos(models.Model):
    Productos_id = models.ForeignKey(Productos, on_delete=models.CASCADE)
    Pedidos_id = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
