from django.contrib import admin
from .models import Producto, Carrito, ItemCarrito, Orden, ItemOrden, Marca, Categoria

# Register your models here.
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Orden)
admin.site.register(ItemOrden)
admin.site.register(Marca)
admin.site.register(Categoria)
