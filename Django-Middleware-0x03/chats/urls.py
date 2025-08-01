from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Main router for conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
messages_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
messages_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(messages_router.urls)),
]
