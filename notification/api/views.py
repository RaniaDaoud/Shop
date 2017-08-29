from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from notification.api.serializers import NotifListSerializer
from notification.models import Notification


class NotifListAPI(ListAPIView):
	def get(self, request, username ,format=None):
		notifs = Notification.objects.filter(to_user__username=username)
		serializer = NotifListSerializer(notifs, many=True)
		serializer_data = serializer.data
		custom_data = {'notifs' : serializer_data }
		return Response(custom_data)