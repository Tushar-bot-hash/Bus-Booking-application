from rest_framework import serializers
from users.models import User # This is the critical line: IMPORT, don't DEFINE

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'is_active')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone')

    def create(self, validated_data):
        # This calls the UserManager.create_user method in your models.py
        return User.objects.create_user(**validated_data)