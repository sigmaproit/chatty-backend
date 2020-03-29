# from django.core.mail import send_mail
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from clinic_system_base.core.async_utilities import call_async
# from django.conf import settings
# from message.models import Message
# from clinic_system_base.notification.managers.notification_supplier import send_notification
#
#
# # If there will be differentiation between patients and nurses in emails sent create special signals\
# @receiver(post_save, sender=Message)
# def new_message(sender, instance, created, raw, using, update_fields, **kwargs):
#     if created:
#         try:
#             # customer = None
#             # for field in settings.CUSTOMER_MODEL.get_fields():
#             #     if field.related_model == settings.AUTH_USER_MODEL:
#             #         customer = settings.CUSTOMER_MODEL.filter(**{field.name: instance.recipient}).all()
#             #     if field.related_model == settings.MESSAGING_GROUPING_MODEL:
#             #         grouping_entity = settings.CUSTOMER_MODEL.filter(**{field.name: instance.recipient}).all()
#             # # Case: Customer is the recipient
#             # if customer:
#             #     notification_title =grouping_entity.name
#             # # Case: Patient is the sender
#             # else:
#             #     patient = Patient.objects.filter(user=instance.sender).first()
#             #     notification_title = patient.display_name
#
#             notification_title = 'New Message'
#
#             mail_title = 'New Message'
#             mail_content = 'You have received a new message from ' + notification_title \
#                            + ', please log in to the app to view it'
#             call_async(send_mail, args=(mail_title, mail_content, settings.EMAIL_HOST_USER, [instance.recipient.email]))
#
#             notification_message = instance.content
#
#             message_dict = {
#                 "source": "notification",
#                 "id": instance.id,
#                 "content": instance.content,
#                 "created_at": str(instance.created_at.isoformat()),
#             }
#
#             # unique ID for the notification, used for grouping
#             notification_id = instance.id
#
#             call_async(send_notification,
#                        args=[notification_message, notification_title, [instance.recipient], True,
#                              dict(message_dict=message_dict, notId=notification_id)])
#         except Exception as e:
#             raise e
