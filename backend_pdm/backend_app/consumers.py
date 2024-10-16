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

    def add_notification(self, event):
        message = event['message']
        message = {
            "employee": message,
            "type": "add"
        }
        self.send(text_data=json.dumps({
            'message': message
        }))

    def update_notification(self, event):
        message = event['message']
        message = {
            "employee": message,
            "type": "update"
        }
        self.send(text_data=json.dumps({
            'message': message
        }))