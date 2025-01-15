import json
import sys
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from urllib.parse import parse_qs

from .constants import GROUP_NAME
from channels.db import database_sync_to_async

class EmployeeConsumer(WebsocketConsumer):
    
    def get_token_from_query_string(self, query_string):
        parsed_query = parse_qs(query_string.decode('utf-8'))
        token = parsed_query.get('token', [None])[0]
        return token
    
    async def authenticate_user(self, token):
        try:
            user = await database_sync_to_async(self._authenticate_user)(token)
            return user
        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid token.")

    def _authenticate_user(self, token):
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        print("Validated token " + str(validated_token))
        user = jwt_auth.get_user(validated_token)
        return user

    def connect(self):
        print("SSSSS", file=sys.stderr)
        self.group_name = GROUP_NAME
        token = self.get_token_from_query_string(self.scope['query_string'])
        print("Token " + token, file=sys.stderr)
        if not token:
            self.close()
            return

        try:
            user = self.authenticate_user(token)
            print("TTTTTTTTT")
            self.user = user
        except AuthenticationFailed:
            self.close()

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