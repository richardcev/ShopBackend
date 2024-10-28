from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter, DateTimeFilter, BaseInFilter
from unidecode import unidecode
from .models import Producto

class ProductoFilter(FilterSet):
    name = CharFilter(method='filter_by_name')
    precio_min = NumberFilter(field_name="precio", lookup_expr='gte')
    precio_max = NumberFilter(field_name="precio", lookup_expr='lte')
    price_ranges = CharFilter(method='filter_by_price_ranges')
    marca = BaseInFilter(field_name="marca", lookup_expr="in") 

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_min', 'precio_max', 'categoria', 'marca', 'subcategoria']

    #Filtro para barra de búsqueda.
    def filter_by_name(self, queryset, name, value):
        matching_products = []
        for producto in queryset:
            palabras = producto.nombre.split(" ")
            for palabra in palabras:
                if unidecode(palabra.lower()) == unidecode(value):
                    matching_products.append(producto)
        return queryset.filter(id__in=[producto.id for producto in matching_products])
    
    def filter_by_price_ranges(self, queryset, name, value):
        # value será una cadena como: "0-21,21-41,201"
        price_ranges = value.split(',')
        print(price_ranges)
        
        # Inicializamos un queryset vacío que acumule los filtros de cada rango.
        price_querysets = []

        # Recorremos los rangos de precio.
        for price_range in price_ranges:
            if '-' in price_range:
                min_price, max_price = map(float, price_range.split('-'))
                price_querysets.append(queryset.filter(precio__gte=min_price, precio__lte=max_price))
            elif price_range.strip() == '201':  # Comprobar específicamente si es '201'
                price_querysets.append(queryset.filter(precio__gt=201))

        # Si no se han añadido filtros, devolvemos el queryset original
        if not price_querysets:
            return queryset
        
        # Unimos los querysets con `|` (operador OR).
        final_queryset = price_querysets[0]
        for qset in price_querysets[1:]:
            final_queryset |= qset
        
        return final_queryset
