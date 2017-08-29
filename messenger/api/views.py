from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )

from messenger.api.serializers import MsgListSerializer, MsgCreateSerializer
from messenger.models import Message
from django.contrib.auth.models import User


class MsgListAPI(ListAPIView):
    def get(self, request, username ,format=None):
        msgs = Message.objects.filter(user__username=username)
        serializer = MsgListSerializer(msgs, many=True)
        serializer_data = serializer.data
        custom_data = {'msgs' : serializer_data }
        return Response(custom_data)

class MsgCreateAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MsgCreateSerializer
   
 
    def post(self, request, to_user):
        serializer = MsgCreateSerializer(data=request.data)
        serializer2 = MsgCreateSerializer(data=request.data)
        user = User.objects.get(username = to_user)
        # conversation = username
        # user = self.request.user
        # # from_user = 
        # # buser=user.buser
        # # shop=Shop.objects.filter(owner=buser.id)
        # serializer.save(user=user, from_user=user,conversation=conversation )
        # serializer.save(user=user, from_user=conversation,conversation=conversation )
        if serializer.is_valid() and serializer2.is_valid():
            serializer.save(user=request.user,from_user=request.user,conversation= user)
            serializer2.save(user=user,from_user=request.user ,conversation= request.user)
            #serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    