from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username']
    ordering_fields = ['created_at']
    lookup_field = 'conversation_id'  # Ensure conversation_id is used for lookups

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants')

        if not participants or len(participants) < 2:
            return Response(
                {'error': 'A conversation must have at least two participants.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.id not in participants:
            participants.append(request.user.id)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('conversation', 'sender')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        # Only return messages where the user is a participant in the conversation
        return Message.objects.filter(conversation__participants=self.request.user).select_related('conversation', 'sender')

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        if not conversation_id:
            return Response({'error': 'conversation_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user not in conversation.participants.all():
            return Response({'detail': 'You are not a participant of this conversation.'}, status=HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
