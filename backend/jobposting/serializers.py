from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth.models import User
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer):
        model = User
        fields = ["id", "email", "password"]
