from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, VerifyEmailView, ResendVerificationCodeView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/resend-verification/', ResendVerificationCodeView.as_view(), name='resend-verification'),
]