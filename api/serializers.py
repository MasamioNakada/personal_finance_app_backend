from rest_framework import serializers
from .models import Category, Budget, Transaction, Tag, FinancialGoal, ChangeLog, UserProfile
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'category_type']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'user', 'name']

class TransactionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

class FinancialGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        fields = '__all__'

class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True, max_length=20, source='userprofile.phone_number')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True}  # Username will be auto-generated from email
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        username = validated_data.get('email').split('@')[0]
        validated_data['username'] = username
        
        user = User.objects.create_user(**validated_data)
        
        UserProfile.objects.create(
            user=user,
            phone_number=profile_data.get('phone_number')
        )
        
        return user
