from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from shop.api.serializers import ProductListSerializer, DetailListSerializer
from shop.models import Produit


class ProductListAPI(ListAPIView):
	def get(self, request, format=None):
		products = Produit.objects.filter(is_favorite=True)
		serializer = ProductListSerializer(products, many=True)
		serializer_data = serializer.data
		custom_data = {'products' : serializer_data }
		return Response(custom_data)


class DetailListAPI(ListAPIView):
	def get(self, request, prod_id ,format=None):
		product = Produit.objects.get(id=prod_id)
		serializer = DetailListSerializer(product)
		serializer_data = serializer.data
		custom_data = {'product' : serializer_data }
		return Response(custom_data)
