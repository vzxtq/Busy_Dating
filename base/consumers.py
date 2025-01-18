import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "group_chat"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        Message.objects.all()
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        return Message.objects.create(sender=user, message=message)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")

        new_message = await self.save_message(username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': new_message.message,
                'username': username,
                'time': new_message.timestamp.strftime('%H:%M')
            }
        )

    async def send_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time
        }))
