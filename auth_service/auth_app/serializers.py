from rest_framework import serializers

from .models import User
from .utils import logger


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        """Create a new user and generate a verification code"""
        username = validated_data['email'].split('@')[0]  # Generate username from email
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
        )
        user.generate_otp()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required")

        return {"email": email, "password": password}


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        """Check verification code"""
        email = data["email"]
        otp = data["otp"]

        try:
            user = User.objects.get(email=email)
            if user.verified:
                raise serializers.ValidationError("Пользователь уже авторизирован")
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        if user.email_otp != otp:
            raise serializers.ValidationError("Неверный код подтверждения.")

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'verified']