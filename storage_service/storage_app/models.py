import uuid
from django.db import models
from .utils import logger
from config import s3_storage


def generate_unique_name(instance, filename):
    """Create a new file name with unique uuid"""
    ext = filename.split('.')[-1]
    return f'{instance.uuid}.{ext}'


class UploadedFile(models.Model):
    """
    File model synchronized with Yandex Cloud's S3 storage.
    When a file is uploaded to the database, it is automatically uploaded to the cloud with the same name.

    uuid - Field for generating a unique key.
    file - The file itself, which is uploaded with a unique name using upload_to.
    profile - Each file is associated with a specific user.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    file = models.FileField(upload_to=generate_unique_name,storage=s3_storage.MediaStorage())



