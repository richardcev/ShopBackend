# serializers.py
from rest_framework import serializers
from .models import Producto, Categoria, SubCategoria, CustomUser

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen', 'stock', 'categoria', 'categoria_nombre', 'marca', 'subcategoria', 'destacado']

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