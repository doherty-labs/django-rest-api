from unittest.mock import MagicMock

from injector import Module, provider, singleton

from django_project import settings
from rest_api.services.cdn import CdnStorage


class CdnObjectStorageModule(Module):
    @singleton
    @provider
    def get_instance(self) -> CdnStorage:
        return CdnStorage(
            bucket_name=settings.CDN_BUCKET_NAME,
            aws_access_key_id=settings.CDN_BUCKET_KEY,
            aws_secret_access_key=settings.CDN_BUCKET_SECRET,
            endpoint_url=settings.CDN_BUCKET_ENDPOINT,
            region_name=settings.CDN_BUCKET_REGION,
        )


class TestCdnObjectStorageModule(Module):
    @singleton
    @provider
    def get_instance(self) -> CdnStorage:
        return MagicMock()
