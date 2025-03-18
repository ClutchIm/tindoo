import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
    """
    Custom user model.
    - Uses email as a unique identifier (USERNAME_FIELD).
    - The 'verified' field indicates whether the email is confirmed.
    - The 'email_otp' field stores a one-time verification code.
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
        """Generates a 6-digit verification code"""
        self.email_otp = str(random.randint(100000, 999999))
        self.otp_created_at = now()
        self.save()

    def verify_code(self, entered_code):
        """Checks if the entered code is correct"""
        return self.email_otp == entered_code