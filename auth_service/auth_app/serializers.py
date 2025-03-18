from rest_framework import serializers
from .models import User
from .utils import logger


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        """Создание нового пользователя и генерация кода верификации"""
        username = validated_data['email'].split('@')[0]  # Генерируем username из email
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.generate_otp()
        return user


class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def validate_otp(self, otp):
        """Проверяем, совпадает ли код"""
        user = self.context['request'].user  # Берём текущего пользователя
        if user.email_otp != otp:
            raise serializers.ValidationError("Неверный код подтверждения.")
        return otp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'verified']
        read_only_fields = ('id',)



