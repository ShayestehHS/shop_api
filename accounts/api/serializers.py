from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()()


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_superuser']
