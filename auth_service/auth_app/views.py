from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .utils import logger, send_verification_email
from .models import User
from .serializers import RegisterSerializer, UserSerializer, VerifyEmailSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(APIView):
    """Регистрация пользователя"""
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user)

            return Response(
                {'message': 'Пользователь создан. Проверьте почту для подтверждения.'},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(APIView):
    """Повторная отправка кода"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.verified:
            return Response({"detail": "Email уже подтвержден"}, status=400)

        send_verification_email(user)
        return Response({"detail": "Код повторно отправлен"}, status=200)


class VerifyEmailView(APIView):
    """Подтверждение кода"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.email_otp != serializer.validated_data['otp']:
                return Response({"detail": "Неверный код"}, status=400)

            user.verified = True
            user.save()
            return Response({"detail": "Email подтвержден"}, status=200)

        return Response(serializer.errors, status=400)


