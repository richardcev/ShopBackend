from django.shortcuts import render
from .models import Producto, Marca, Categoria, SubCategoria
from django.http import JsonResponse
from unidecode import unidecode
from .serializers import ProductoSerializer, CategoriaSerializer, SubCategoriaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from .filters import ProductoFilter

class Productos(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id' ,'nombre', 'precio', 'categoria', 'marca', 'subcategoria']
    filterset_class = ProductoFilter

    def get_queryset(self):
        queryset = Producto.objects.all()
        return queryset

# def categorias(request):
#     categorias = Categoria.objects.all()
#     data = {'categorias': []}
    
#     for categoria in categorias:
#         subcategorias = SubCategoria.objects.filter(categoria=categoria)
#         categoria_data = {
#             'id': categoria.id,
#             'nombre': categoria.nombre,
#             'descripcion': categoria.descripcion,
#             'subcategorias': list(subcategorias.values())
#         }
#         data['categorias'].append(categoria_data)
    
#     return JsonResponse(data)

class CategoriasViewset(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id' ,'nombre', 'descripcion']

    def get_queryset(self):
        queryset = Categoria.objects.all()
        return queryset
    
class SubCategoriasViewset(viewsets.ModelViewSet):
    serializer_class = SubCategoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id' ,'nombre', 'descripcion']

    def get_queryset(self):
        queryset = SubCategoria.objects.all()
        return queryset