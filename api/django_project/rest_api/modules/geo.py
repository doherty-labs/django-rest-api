from unittest.mock import MagicMock

from django.conf import settings
from injector import Module, provider, singleton

from rest_api.services.geo import GeoPyService


class GeoModule(Module):
    @singleton
    @provider
    def geo_instance(self) -> GeoPyService:
        return GeoPyService(api_key=settings.GMAPS_API_KEY)


class TestGeoModule(Module):
    @singleton
    @provider
    def geo_instance(self) -> GeoPyService:
        return MagicMock()
