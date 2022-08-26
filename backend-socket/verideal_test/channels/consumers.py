import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ProcessConsumer(WebsocketConsumer):
    def connect(self):
        self.id = "room" # self.scope['url_route']['kwargs']['id']

        # Join group
        async_to_sync(self.channel_layer.group_add)(
            self.id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)

        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            self.id,
            {
                'type': 'process_percent',
                'id': data['id']
            }
        )

    # Receive message from  group
    def process_percent(self, event):

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
