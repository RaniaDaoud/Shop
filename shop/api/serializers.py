from rest_framework.serializers import ModelSerializer


from shop.models import Produit


class ProductListSerializer(ModelSerializer):
	class Meta:
		model = Produit
		fields = ('id', 'title', 'descreption', 'prix', 'quantite', 'created')

class DetailListSerializer(ModelSerializer):
	class Meta:
		model = Produit
		fields = ('id', 'title', 'descreption', 'prix', 'quantite', 'created','logo', 'reaction_set')		
