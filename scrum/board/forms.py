import django_filters

from .models import Product
from rest_framework import filters


class ProductFilter(django_filters.FilterSet):	
	max_price = django_filters.NumberFilter(name="price", lookup_expr='lte')
	min_price = django_filters.NumberFilter(name="price", lookup_expr='gte')
	
	class Meta:
		model = Product
		fields = ('category','name','min_price','max_price')
