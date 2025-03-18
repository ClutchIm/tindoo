from django.contrib.auth import authenticate
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import logger, send_verification_email
from .models import User
from .serializers import RegisterSerializer, UserSerializer, VerifyEmailSerializer, LoginSerializer


class UserViewSet(ReadOnlyModelViewSet):
    """User information"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(APIView):
    """User registration"""
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


class LoginView(APIView):
    """User login"""
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user_email = validated_data["email"]
            user_password = validated_data["password"]

            user = authenticate(username=user_email, password=user_password)
            if user:
                refresh = RefreshToken.for_user(user)
                response = Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
                response.set_cookie("jwt", str(refresh.access_token), httponly=True, secure=True)
                return response

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Logout (add refresh token to blacklist)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("jwt")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                response = Response({"message": "Вы успешно вышли"}, status=status.HTTP_205_RESET_CONTENT)
                response.delete_cookie("jwt")
                return response
            return Response({"error": "Токен отсутствует"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Ошибка выхода"}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(APIView):
    """Resend verification code"""
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            if user.verified:
                return Response({"detail": "Email уже подтвержден"}, status=status.HTTP_400_BAD_REQUEST)
            user.generate_otp()
            send_verification_email(user)
            return Response({"detail": "Код повторно отправлен"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class VerifyEmailView(APIView):
    """Email verification"""
    permission_classes = []

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = User.objects.get(email=request.data['email'])
            if user.verify_code(serializer.validated_data['otp']):
                user.verified = True
                user.is_active = True
                user.save()
                return Response({"detail": "Email подтвержден"}, status=status.HTTP_200_OK)
            return Response({"detail": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


