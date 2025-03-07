from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Budget, Category, Tag, Transaction, FinancialGoal, ChangeLog
from .serializers import BudgetSerializer,CategorySerializer,TagSerializer , TransactionSerializer, FinancialGoalSerializer, ChangeLogSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password', 'first_name', 'last_name'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password', format='password'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
        }
    ),
    responses={
        201: openapi.Response('Successful registration', UserSerializer),
        400: openapi.Response('Invalid data'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data.copy()
    email = data.get('email')
    
    if email:
        # Extract username from email (everything before @)
        username = email.split('@')[0]
        data['username'] = username
    
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        # Update first_name and last_name
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        user.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['login', 'password'],
        properties={
            'login': openapi.Schema(type=openapi.TYPE_STRING, description='Email or Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password', format='password'),
        }
    ),
    responses={
        200: openapi.Response('Successful login', UserSerializer),
        401: openapi.Response('Invalid credentials'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    login = request.data.get('login')
    password = request.data.get('password')
    
    # Try to authenticate with username
    user = authenticate(username=login, password=password)
    
    # If authentication fails, try with email
    if not user:
        from django.contrib.auth.models import User
        try:
            username = User.objects.get(email=login).username
            user = authenticate(username=username, password=password)
        except User.DoesNotExist:
            pass
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class FinancialGoalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FinancialGoalSerializer

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)

class ChangeLogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeLogSerializer

    def get_queryset(self):
        return ChangeLog.objects.filter(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
