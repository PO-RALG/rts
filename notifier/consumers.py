from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # Extract user ID from query parameters
        query_params = self.scope['query_string'].decode('utf-8')
        user_id = query_params.split('=')[1]
        # print("queryyyPPP", user_id)

        # Add the user to a group based on their user ID
        self.group_name = f"user_{user_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        # Remove the user from the group when they disconnect
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def notification_message(self, event):
        # Send notification message to the client
        self.send(text_data=json.dumps(event["message"]))
