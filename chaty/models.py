import swapper
from django.conf import settings
from django.db import models
from django.utils import timezone

from chaty.managers import MessageQueryset


class Message(models.Model):
    created_at = models.DateTimeField('created at date', default=timezone.now, editable=False)
    updated_at = models.DateTimeField('last updated date at', default=timezone.now, editable=True)

    content = models.TextField('content', max_length=1000, blank=True, null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Sender', related_name='sent_messages',
                               related_query_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Recipient', related_name='received_messages',
                                  related_query_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    grouping_entity = models.ForeignKey(swapper.get_model_name('chaty', 'BaseGroupingEntity'), verbose_name='Grouping Entity', related_name='messages',
                                related_query_name='messages', on_delete=models.CASCADE, null=True, blank=True)

    is_read = models.BooleanField('is_read', default=False)

    objects = MessageQueryset.as_manager()

    def update_dict(self, **kwargs):

        for field in kwargs.keys():
            setattr(self, field, kwargs[field])
        return self


class BaseGroupingEntity(models.Model):
    # minimal base implementation ...
    class Meta:
        swappable = swapper.swappable_setting('chaty', 'BaseGroupingEntity')

