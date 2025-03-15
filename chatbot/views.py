from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import ChatSession, Message
from .serializers import MessageSerializer, ChatSessionSerializer
from api.models import UserProfile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def get_dummy_bot_response(message_content):
    """Dummy bot response function for testing purposes."""
    return f"Bot received: {message_content}. This is a dummy response."

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['phone_number', 'content'],
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
            'message_type': openapi.Schema(type=openapi.TYPE_STRING, description='Message type (default: text)', default='text'),
        }
    ),
    responses={
        201: openapi.Response(
            'Messages created successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_message': openapi.Schema(type=openapi.TYPE_OBJECT, description='User message details'),
                    'bot_response': openapi.Schema(type=openapi.TYPE_OBJECT, description='Bot response details')
                }
            )
        ),
        400: 'Bad Request - Missing required fields',
        404: 'Not Found - User not found with provided phone number'
    }
)
@api_view(['POST'])
def chattwilio(request):
    """Endpoint for handling chat interactions with the bot."""
    phone_number = request.data.get('phone_number')
    if not phone_number:
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_profile = UserProfile.objects.get(phone_number=phone_number)
        user = user_profile.user
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found with this phone number'}, status=status.HTTP_404_NOT_FOUND)

    message_type = request.data.get('message_type', 'text')
    content = request.data.get('content')

    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Get or create active chat session
    active_session = ChatSession.objects.filter(
        user=user,
        status='active'
    ).first()

    if not active_session:
        active_session = ChatSession.objects.create(user=user)

    # Create user message
    user_message = Message.objects.create(
        session=active_session,
        sender_type='user',
        message_type=message_type,
        content=content
    )

    # Generate and save bot response
    bot_response = get_dummy_bot_response(content)
    bot_message = Message.objects.create(
        session=active_session,
        sender_type='bot',
        message_type='text',
        content=bot_response
    )

    # Serialize and return both messages
    return Response({
        'user_message': MessageSerializer(user_message).data,
        'bot_response': MessageSerializer(bot_message).data
    }, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['content'],
        properties={
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
            'message_type': openapi.Schema(type=openapi.TYPE_STRING, description='Message type (default: text)', default='text'),
        }
    ),
    responses={
        201: openapi.Response(
            'Messages created successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_message': openapi.Schema(type=openapi.TYPE_OBJECT, description='User message details'),
                    'bot_response': openapi.Schema(type=openapi.TYPE_OBJECT, description='Bot response details')
                }
            )
        ),
        400: 'Bad Request - Missing required fields',
        401: 'Unauthorized - Authentication credentials were not provided'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatweb(request):
    """Endpoint for handling web-based chat interactions with the bot."""
    user = request.user
    message_type = request.data.get('message_type', 'text')
    content = request.data.get('content')

    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Get or create active chat session
    active_session = ChatSession.objects.filter(
        user=user,
        status='active'
    ).first()

    if not active_session:
        active_session = ChatSession.objects.create(user=user)

    # Create user message
    user_message = Message.objects.create(
        session=active_session,
        sender_type='user',
        message_type=message_type,
        content=content
    )

    # Generate and save bot response
    bot_response = get_dummy_bot_response(content)
    bot_message = Message.objects.create(
        session=active_session,
        sender_type='bot',
        message_type='text',
        content=bot_response
    )

    # Serialize and return both messages
    return Response({
        'user_message': MessageSerializer(user_message).data,
        'bot_response': MessageSerializer(bot_message).data
    }, status=status.HTTP_201_CREATED)
