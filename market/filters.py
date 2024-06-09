import django_filters
from unidecode import unidecode
from .models import Producto

class ProductoFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'categoria', 'marca', 'subcategoria']

    def filter_by_name(self, queryset, name, value):
        matching_products = []
        for producto in queryset:
            palabras = producto.nombre.split(" ")
            for palabra in palabras:
                if unidecode(palabra.lower()) == unidecode(value):
                    matching_products.append(producto)
        return queryset.filter(id__in=[producto.id for producto in matching_products])
