from rest_framework.serializers import ModelSerializer


from messenger.models import Message


class MsgListSerializer(ModelSerializer):
	class Meta:
		model = Message
		fields = ('id', 'user', 'message', 'objet', 'from_user', 'date')


class MsgCreateSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ( 'message', 'produit', 'date')
