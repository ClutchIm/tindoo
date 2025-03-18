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
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        """Проверяем, существует ли пользователь с таким email и совпадает ли OTP-код"""
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        if user.email_otp != data['otp']:
            raise serializers.ValidationError("Неверный код подтверждения.")

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'verified']
        read_only_fields = ('id',)



