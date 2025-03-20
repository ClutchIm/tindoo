from rest_framework import serializers
from .models import UploadedFile
from .utils import logger


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'
