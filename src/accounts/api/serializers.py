from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    email = None

    class Meta:
        model = User
        fields = ['username', 'password']
