from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )

from reaction.api.serializers import ReactionCreateSerializer
from reaction.models import Reaction
from django.contrib.auth.models import User
from shop.models import Produit




class ReactionCreateAPIView(CreateAPIView):
    #queryset = Reaction.objects.all()
    serializer_class = ReactionCreateSerializer
   
 
    def post(self, request, prod_id):
        serializer = ReactionCreateSerializer(data=request.data)
        produit = Produit.objects.get(id=prod_id)

        
        if serializer.is_valid() :
            serializer.save(user=request.user, produit=produit)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    