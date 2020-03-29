from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from chaty.models import Message
from chaty.serializers import MessageSerializer
from chaty.utilities import get_grouping_entity_from_request


class StaffMessageView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        customer_user_id = self.kwargs.get('customer_user_id')
        return Message.objects.customer_chat_with_grouping_entity(customer_user_id)

    def create(self, request, *args, **kwargs):
        customer_user_id = self.kwargs.get('customer_user_id')
        request.data['grouping_entity'] = get_grouping_entity_from_request(request)
        request.data['sender'] = request.user.id
        request.data['recipient'] = customer_user_id
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['patch'])
    def read_all(self, request, customer_user_id):
        chat_messages = self.get_queryset().filter(is_read=False)
        for msg in chat_messages:
            if msg.sender_id == customer_user_id:
                msg.is_read = True
                msg.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def unread_latest(self, request, customer_user_id):
        chat_message = self.get_queryset().filter(sender=customer_user_id).order_by('-id').first()
        if chat_message:
            chat_message.is_read = False
            chat_message.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def unread_messages_count(self, request):
        grouping_entity = get_grouping_entity_from_request(request)
        pairs = Message.objects.grouping_entity_unread_counts_pairs(grouping_entity).all()
        return Response(status=status.HTTP_200_OK, data=pairs)
