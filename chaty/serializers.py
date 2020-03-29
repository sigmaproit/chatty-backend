from django.apps import apps
from django.conf import settings
from rest_framework import serializers

from chaty.models import Message
from chaty.utilities import get_model_from_app_model_name


class MessageSerializer(serializers.ModelSerializer):
    sender_display_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'content', 'sender', 'recipient', 'grouping_entity', 'created_at', 'is_read',
                  'sender_display_name')

    @classmethod
    def get_sender_display_name(cls, message):
        # TODO: see if you can get a method from user that takes id and returns display_name
        # if not settings.STAFF_MODEL or not settings.STAFF_DISPLAY_NAME_FIELD:
        #     return None
        # staff_model = get_model_from_app_model_name(settings.STAFF_MODEL)
        # staff = StaffDataSerializer(instance=message.sender).data
        # if staff:
        #     return staff['user_data']['display_name']
        # if not settings.STAFF_APP_NAME:
        #     return None
        # staff_app = apps.get_app_config(settings.STAFF_APP_NAME)
        # return staff_app.get_display_name_from_user_id(message.sender_id)
        return None
