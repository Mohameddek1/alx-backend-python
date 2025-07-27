from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Assumes the object has a `conversation` attribute
        conversation = getattr(obj, 'conversation', None)
        if conversation is None:
            return False
        return request.user in conversation.participants.all()
