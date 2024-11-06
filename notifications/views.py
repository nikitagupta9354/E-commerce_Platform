from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class NotificationAPIView(APIView):
    permission_classes = [IsAdminUser]  

    def post(self, request):
        message = request.data.get("message")
        if not message:
            return Response({"error": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Sending message to the WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notification_group",  # The group name where users are connected
            {
                "type": "send_notification",
                "message": message
            }
        )
        return Response({"success": "Notification sent."}, status=status.HTTP_200_OK)
