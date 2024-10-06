import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .constants import GROUP_NAME

class EmployeeConsumer(WebsocketConsumer):
    
    def connect(self):
        self.group_name = GROUP_NAME

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        type_message = text_data_json["type"]
        message = text_data_json["message"]
        
        if type_message in ["ADD", "UPDATE"]:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "send_notification", "message": message}
            )

    def send_notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))