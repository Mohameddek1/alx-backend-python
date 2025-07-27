from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    For unsafe methods (PUT, PATCH, DELETE), user must be a participant.
    """

    def has_permission(self, request, view):
        # Allow authenticated users for safe methods, check object for unsafe
        if request.method in ("PUT", "PATCH", "DELETE"):
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For PUT, PATCH, DELETE, only allow if user is a participant
        if request.method in ("PUT", "PATCH", "DELETE"):
            conversation = getattr(obj, 'conversation', None)
            if conversation is None:
                return False
            return request.user in conversation.participants.all()
        # For other methods, fallback to previous logic
        conversation = getattr(obj, 'conversation', None)
        if conversation is None:
            return False
        return request.user in conversation.participants.all()
