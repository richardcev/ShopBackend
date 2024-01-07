from django.shortcuts import render
from .models import Producto, Marca, Categoria
from django.http import JsonResponse
import json
from unidecode import unidecode


# Create your views here.

def productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': [
            productoFinal(request, producto)
            for producto in productos
        ]
    }
    return JsonResponse(data)

def producto(request, id):
    producto = Producto.objects.get(id=id)
    print(producto)
    data = {'producto' : productoFinal(request, producto)}
    return JsonResponse(data)


def categorias(request):
    categorias= Categoria.objects.all()
    data={'categorias': list(categorias.values())}
    return JsonResponse(data)


def filter_categoria(request, cat):
    categoria = Categoria.objects.get(nombre=cat)
    id_categoria = categoria.id
    productos= Producto.objects.filter(categoria= id_categoria)
    data = {
        'productos': [
            productoFinal(request, producto)
            for producto in productos
        ]
    }
    return JsonResponse(data)


def search_producto(request):
    filtro = request.GET.get('text')  # Obtiene el valor de búsqueda del objeto JSON
    productos = Producto.objects.all()  # Filtra los productos que contienen el filtro en el nombre
    data = {'productos': []}

    for producto in productos:
        palabras= producto.nombre.split(" ")
        for palabra in palabras:
            if unidecode(palabra.lower())==unidecode(filtro):
                producto_data = productoFinal(request, producto)
                data['productos'].append(producto_data)

    return JsonResponse(data)


def productoFinal(request, producto):
    productofinal= {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'precio': producto.precio,
                    'imagen': request.build_absolute_uri(producto.imagen.url),
                    'stock': producto.stock,
                    'categoria': producto.categoria.nombre,
                    'marca': producto.marca.nombre
                }
    return productofinal
    
