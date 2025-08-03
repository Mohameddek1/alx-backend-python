from .models import Message
from django.db.models import Prefetch

# Optimized query for top-level messages and their replies

def get_threaded_conversations(user):
    messages = (
        Message.objects.filter(receiver=user, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
        .order_by('-timestamp')
    )
    return messages

# Recursive function to fetch all replies to a message

def get_all_replies(message):
    replies = list(message.replies.all())
    all_replies = []
    for reply in replies:
        all_replies.append(reply)
        all_replies.extend(get_all_replies(reply))
    return all_replies
