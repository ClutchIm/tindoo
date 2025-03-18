import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    - email используется как уникальный идентификатор (USERNAME_FIELD).
    - verified показывает, подтверждена ли почта.
    - email_otp хранит одноразовый код для верификации.
    """

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def generate_otp(self):
        """Генерирует 6-значный код для верификации"""
        self.email_otp = str(random.randint(100000, 999999))
        self.otp_created_at = now()
        self.save()

    def verify_code(self, entered_code):
        """Проверяем введенный код"""
        return self.email_otp == entered_code