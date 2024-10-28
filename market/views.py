from django.shortcuts import render
from .models import Producto, Marca, Categoria, SubCategoria, CustomUser, DescripcionProducto
from .serializers import ProductoSerializer, CategoriaSerializer, SubCategoriaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from .filters import ProductoFilter
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer, DescripcionProductoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError


class Productos(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id' ,'nombre', 'categoria', 'marca', 'subcategoria']
    filterset_class = ProductoFilter

    def get_queryset(self):
        queryset = Producto.objects.all()
        return queryset
    
class DetalleProductoViewSet(viewsets.ModelViewSet):
    serializer_class = DescripcionProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id' , 'producto']

    def get_queryset(self):
        queryset = DescripcionProducto.objects.all()
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
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Asegura que solo los usuarios autenticados puedan acceder a este endpoint

    def get(self, request, *args, **kwargs):
        user = request.user  # Obtén el usuario autenticado desde el request
        serializer = UserSerializer(user)  # Usa un serializer para convertir el usuario en datos JSON
        return Response(serializer.data, status=status.HTTP_200_OK)
    

      
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = None
            
            if user is not None and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            nombres = serializer.validated_data['nombres']
            apellidos = serializer.validated_data['apellidos']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            tipo_documento = serializer.validated_data['tipo_documento']
            documento = serializer.validated_data['documento']

            username = email.split("@")[0]

            user = CustomUser(
                username=username,
                first_name=nombres,
                last_name=apellidos,
                email=email,
                tipo_documento=tipo_documento,
                documento=documento
            )
            user.set_password(password)
            user.save()

            return Response({'message': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)