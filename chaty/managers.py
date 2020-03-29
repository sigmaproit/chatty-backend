from django.db import models
from django.db.models import Case, When, Value, BooleanField, Count, Q


class MessageQueryset(models.QuerySet):
    def customer_chat_with_grouping_entity(self, customer_user_id):
        return self.filter(models.Q(sender=customer_user_id) | models.Q(recipient=customer_user_id)) \
            .order_by('-created_at')

    def grouping_entity_unread_counts_pairs(self, grouping_entity):
        query = self
        if grouping_entity:
            query = query.filter(grouping_entity=grouping_entity)
        return query.extra(
            select={
                'sender_user_id': 'chaty_message.sender_id'
            }
        ).values('sender_user_id').annotate(count=Count('is_read', filter=Q(is_read=False)))

    def customer_unread_counts_pairs(self, customer_user_id):
        return self.filter(recipient=customer_user_id).extra(
            select={
                'sender_user_id': 'chaty_message.sender_id'
            }
        ).values('sender_user_id').annotate(count=Count('is_read', filter=Q(is_read=False)))
