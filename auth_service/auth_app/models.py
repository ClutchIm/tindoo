from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def generate_otp(self):
        """Генерирует 6-значный код для верификации"""
        self.email_otp = str(uuid.uuid4().int)[:6]  # Берем первые 6 цифр от UUID
        self.save()