import logging
from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(user):
    """Отправляет код подтверждения"""
    code = user.email_otp

    # Отправляем email
    send_mail(
        subject="Код подтверждения",
        message=f"Ваш код: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

logger = logging.getLogger("auth_service")