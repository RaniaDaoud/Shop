from rest_framework.serializers import ModelSerializer


from notification.models import Notification


class NotifListSerializer(ModelSerializer):
	class Meta:
		model = Notification
		fields = ('id', 'from_user', 'to_user', 'product', 'type', 'date', 'is_read')