from unittest.mock import MagicMock

from injector import Module, provider, singleton

from rest_api.services.nylas import NylasService


class NylasModule(Module):
    @singleton
    @provider
    def get_instance(self) -> NylasService:
        return NylasService()


class TestNylasModule(Module):
    @singleton
    @provider
    def get_instance(self) -> NylasService:
        return MagicMock()
