from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Producto, Carrito, ItemCarrito, Orden, ItemOrden, Marca, Categoria, SubCategoria, CustomUser, DescripcionProducto

# Register your models here.
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Orden)
admin.site.register(ItemOrden)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(DescripcionProducto)
admin.site.register(CustomUser, UserAdmin)
