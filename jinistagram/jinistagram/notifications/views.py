from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # django status code
from . import models, serializers

class Notifications(APIView):
    def get(self,request, format=None):
        # to의 대상일때 알림
        user = request.user
        notifications = models.Notification.objects.filter(to=user)
        serializer = serializers.NotificationSerializer(notifications, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)