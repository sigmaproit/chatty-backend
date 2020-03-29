from django.conf import settings
from django.utils import timezone

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from channels.layers import get_channel_layer
from rest_framework import exceptions

from chaty.serializers import MessageSerializer
from chaty.utilities import get_model_from_app_model_name


def save_message_in_db(content, grouping_entity_id, sender_id, recipient_id=None):
    validated_data = dict(grouping_entity=grouping_entity_id, sender=sender_id, recipient=recipient_id,
                          content=content)
    msg_serializer = MessageSerializer(data=validated_data)
    msg_serializer.is_valid(True)
    msg_instance = msg_serializer.save()

    return msg_instance


def get_subjected_costumers(grouping_entity):
    customer_model = get_model_from_app_model_name(settings.CUSTOMER_MODEL) if hasattr(settings, 'CUSTOMER_MODEL') else None
    grouping_model = get_model_from_app_model_name(settings.MESSAGING_GROUPING_MODEL) if hasattr(settings, 'MESSAGING_GROUPING_MODEL') else None
    customers = []
    if grouping_model and grouping_entity:
        for field in customer_model._meta.get_fields():
            if field.related_model == grouping_model:
                customers = customer_model.objects.filter(**{field.name: grouping_entity}).all()
    else:
        customers = customer_model.objects.all()

    return customers


class CustomerMessageConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        self.group_name = f'customer{str(user.id)}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

        return self.close(close_code)

    # Receive message from WebSocket
    def receive(self, text_data):
        # if not is_user_authenticated(self.scope['user']):
        #     raise exceptions.AuthenticationFailed('session_expired')

        text_data_json = json.loads(text_data)
        message = text_data_json['content']

        if settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME and settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME in self.scope:
            grouping_entity_id = self.scope[settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME].id
        else:
            grouping_entity_id = None
        msg_instance = save_message_in_db(content=message, grouping_entity_id=grouping_entity_id,
                                          sender_id=self.scope['user'].id)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'content': message,
                'created_at': str(timezone.now().isoformat()),
                'id': msg_instance.id,
                'sender_user_id': msg_instance.sender_id,
                'recipient_user_id': msg_instance.recipient_id
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event
        }))


class StaffMessageConsumer(WebsocketConsumer):
    def connect(self):
        # Management group for staff to send websocket events
        # (used to notify for newly created customer to create a group for him)
        # TODO: May make it a group for all grouping entity staff to share management events
        async_to_sync(self.channel_layer.group_add)(
            str(self.scope['user'].id) + 'management_group',
            self.channel_name
        )
        # Create a group for each grouping entity customer and join all groups
        self.grouping_entity = self.scope[
            settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME] if settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME in self.scope else None
        customers = get_subjected_costumers(self.grouping_entity)
        for customer in customers:
            async_to_sync(self.channel_layer.group_add)(
                f'customer{str(customer.user.id)}',
                self.channel_name
            )

        self.accept()

    def disconnect(self, close_code):
        # Leave all customers groups
        customers = get_subjected_costumers(self.grouping_entity)
        for customer in customers:
            print(customer.id)
            async_to_sync(self.channel_layer.group_discard)(
                f'customer{str(customer.user.id)}',
                self.channel_name
            )
        return self.close()

    # Receive message from WebSocket
    def receive(self, text_data):
        # if not is_user_authenticated(self.scope['user']):
        #     raise exceptions.AuthenticationFailed('session_expired')

        text_data_json = json.loads(text_data)
        message = text_data_json['content']
        customer_user_id = text_data_json['user_id']

        if settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME and settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME in self.scope and \
                self.scope[settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME]:
            grouping_entity_id = self.scope[settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME].id
        else:
            grouping_entity_id = None
        msg_instance = save_message_in_db(content=message,
                                          grouping_entity_id=grouping_entity_id, sender_id=self.scope['user'].id,
                                          recipient_id=customer_user_id, )

        # Ensure that customer has a group
        async_to_sync(self.channel_layer.group_add)(
            f'customer{str(customer_user_id)}',
            self.channel_name
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            f'customer{str(customer_user_id)}',
            {
                'type': 'chat_message',
                'content': message,
                'created_at': str(timezone.now().isoformat()),
                'id': msg_instance.id,
                'sender_user_id': msg_instance.sender_id,
                'recipient_user_id': msg_instance.recipient_id
            }
        )

    # Receive message from room group
    def chat_message(self, event):

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event
        }))

    def add_customer_group(self, event):
        async_to_sync(self.channel_layer.group_add)(
            f'customer{str(event["customer_user_id"])}',
            self.channel_name
        )

    @classmethod
    def add_staff_customer_group(cls, staff_user_id, customer_user_id):
        layer = get_channel_layer()

        # TODO: make for all staff related to customer, not single staff
        async_to_sync(layer.group_send)(str(staff_user_id) + 'management_group', {
            'type': 'add_customer_group',
            'customer_user_id': customer_user_id
        })
