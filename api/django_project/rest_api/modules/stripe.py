from unittest.mock import MagicMock

from injector import Module, provider, singleton

from rest_api.services.stripe import StripeService


class StripeModule(Module):
    @singleton
    @provider
    def get_instance(self) -> StripeService:
        return StripeService()


class TestStripeModule(Module):
    @singleton
    @provider
    def get_instance(self) -> StripeService:
        return MagicMock()
