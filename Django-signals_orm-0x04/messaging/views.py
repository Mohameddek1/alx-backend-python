
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Message
from django.db.models import Prefetch

User = get_user_model()

@login_required
@require_POST
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('login')

# Threaded conversation view
@login_required
def threaded_conversation(request, message_id=None):
    if message_id:
        root_message = get_object_or_404(Message, id=message_id)
        messages = Message.objects.filter(parent_message=root_message).select_related('sender', 'receiver').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
    else:
        messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True).select_related('sender', 'receiver').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )

    def get_all_replies(message):
        replies = list(message.replies.all())
        all_replies = []
        for reply in replies:
            all_replies.append(reply)
            all_replies.extend(get_all_replies(reply))
        return all_replies

    context = {
        'messages': messages,
        'get_all_replies': get_all_replies,
    }
    return render(request, 'messaging/threaded_conversation.html', context)

# Example message creation view for threading
@login_required
@require_POST
def send_message(request):
    content = request.POST.get('content')
    receiver_id = request.POST.get('receiver')
    parent_id = request.POST.get('parent_message')
    receiver = get_object_or_404(User, id=receiver_id)
    parent_message = None
    if parent_id:
        parent_message = get_object_or_404(Message, id=parent_id)
    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content,
        parent_message=parent_message
    )
    return redirect('threaded_conversation')
