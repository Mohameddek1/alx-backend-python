from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

# Log message edits and save old content before update
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message, not an edit
    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if old.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old.content
        )
        instance.edited = True
