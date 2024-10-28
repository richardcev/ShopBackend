from django.db import models
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    def __str__(self):
        return self.nombre
    
class SubCategoria(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
class CustomUser(AbstractUser):
    tipo_documento = models.CharField(max_length=20, blank=True, null=True)
    documento = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

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
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    destacado = models.BooleanField(null=True, blank=True)
    def __str__(self):
        return self.nombre
    
    
    def clean(self):
        # Validar que la subcategoría seleccionada pertenezca a la categoría seleccionada
        if self.subcategoria.categoria != self.categoria:
            raise ValidationError('La subcategoría no pertenece a la categoría seleccionada.')
        
class DescripcionProducto(models.Model):
    caracteristica = models.CharField(max_length=255)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
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
