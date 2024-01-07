from django.db import models
from django.contrib.sessions.models import Session

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion= models.TextField()
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='productos')
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
class Carrito(models.Model):
    session = models.ForeignKey(Session, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')

    def __str__(self):
        return f"Carrito ({self.id})"
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.carrito} - {self.producto}"

class Orden(models.Model):
    session = models.ForeignKey(Session, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    direccion_envio = models.CharField(max_length=200)
    productos = models.ManyToManyField(Producto, through='ItemOrden')

    def __str__(self):
        return f"Orden ({self.id})"


class ItemOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.orden} - {self.producto}"
