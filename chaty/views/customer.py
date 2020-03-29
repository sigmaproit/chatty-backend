from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status

from chaty.models import Message
from chaty.serializers import MessageSerializer
from chaty.utilities import get_grouping_entity_from_request


class CustomerMessageView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.customer_chat_with_grouping_entity(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['grouping_entity'] = get_grouping_entity_from_request(request)
        request.data['sender'] = request.user.id
        # If customer: no need for recipient
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['patch'])
    def read_all(self, request):
        chat_messages = self.get_queryset().filter(is_read=False)
        for msg in chat_messages:
            if msg.sender_id != self.request.user.id:
                msg.is_read = True
                msg.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def unread_messages_count(self, request):
        pairs = Message.objects.customer_unread_counts_pairs(request.user).all()
        return Response(status=status.HTTP_200_OK, data=pairs)
