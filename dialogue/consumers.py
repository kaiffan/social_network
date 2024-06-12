import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from attachments.models import Attachment
from message.models import Message


class DialogueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.dialogue_id = self.scope['url_route']['kwargs']['dialogue_id']
            self.room_group_name = f'dialogue_{self.dialogue_id}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # обновлять время захода в бд

            await self.accept()
        except KeyError as exception:
            print(f"Error: {str(exception)}")
            await self.close(code=404)
        except Exception as exception:
            print(f"Error as connect to dialogue room: {str(exception)}")
            await self.close(code=500)

    async def disconnect(self, close_code):
        print(f"Disconnect from dialogue room: {self.room_group_name}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_sender_id = text_data_json['user_sender_id']
        user_recipient_id = text_data_json['user_recipient_id']
        attachments = text_data_json.get('attachments', [])

        await self.save_message(user_sender_id, user_recipient_id, self.dialogue_id, message, attachments)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_sender_id': user_sender_id,
                'user_recipient_id': user_recipient_id,
                'attachments': attachments
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_sender_id = event['user_sender_id']
        user_recipient_id = event['user_recipient_id']
        attachments = event['attachments']

        await self.send(text_data=json.dumps({
            'message': message,
            'user_sender_id': user_sender_id,
            'user_recipient_id': user_recipient_id,
            'attachments': attachments
        }))

    @sync_to_async
    def save_message(self, id_user_sender, id_user_recipient, dialogue_id, message, attachments):
        message = Message.objects.create(
            text=message,
            user_sender_id=id_user_sender,
            user_recipient_id=id_user_recipient,
            dialogue_id=dialogue_id
        )
        self.save_attachments(attachments=attachments, message_id=message.id)

    def save_attachments(self, attachments, message_id):
        for attachment in attachments:
            Attachment.objects.create(
                attachment_url=attachment.get('attachment_url'),
                attachment_type=attachment.get('attachment_type'),
                message_id=message_id,
            )
