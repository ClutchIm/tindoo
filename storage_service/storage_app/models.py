from django.db import models


class Storage(models.Model):
    """storage model"""
    url = models.URLField()

