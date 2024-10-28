# serializers.py
from rest_framework import serializers
from .models import Producto, Categoria, SubCategoria, CustomUser, DescripcionProducto, Marca


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'descripcion']  

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    sub_categoria_nombre = serializers.CharField(source='subcategoria.nombre', read_only=True)
    marca = MarcaSerializer()
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen', 'stock', 'categoria', 'categoria_nombre', 'marca', 'subcategoria', 'sub_categoria_nombre', 'destacado']


class DescripcionProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescripcionProducto
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class SubCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoria
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class RegisterSerializer(serializers.Serializer):
    nombres= serializers.CharField()
    apellidos= serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tipo_documento= serializers.CharField()
    documento= serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'tipo_documento', 'documento', 'direccion']