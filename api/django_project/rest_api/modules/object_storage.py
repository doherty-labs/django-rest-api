from unittest.mock import MagicMock

from django.conf import settings
from injector import Module, provider, singleton

from rest_api.services.s3 import ObjectStorageService


class ObjectStorageModule(Module):
    @singleton
    @provider
    def get_instance(self) -> ObjectStorageService:
        return ObjectStorageService(
            bucket_name=settings.BUCKET_NAME,
            aws_access_key_id=settings.BUCKET_KEY,
            aws_secret_access_key=settings.BUCKET_SECRET,
            endpoint_url=settings.BUCKET_ENDPOINT,
            region_name=settings.BUCKET_REGION,
        )


class TestObjectStorageModule(Module):
    @singleton
    @provider
    def get_instance(self) -> ObjectStorageService:
        return MagicMock()
