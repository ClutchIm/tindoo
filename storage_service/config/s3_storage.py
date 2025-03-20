from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'media'
    file_overwrite = False  # Файлы не перезаписываются
    default_acl = 'public-read'  # Доступ для чтения


class StaticStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'static'
    file_overwrite = True
    default_acl = 'public-read'