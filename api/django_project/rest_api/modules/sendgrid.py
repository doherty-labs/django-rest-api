from unittest.mock import MagicMock

from injector import Module, provider, singleton

from rest_api.services.sendgrid import EmailService


class EmailModule(Module):
    @singleton
    @provider
    def get_instance(self) -> EmailService:
        return EmailService()


class TestEmailModule(Module):
    @singleton
    @provider
    def get_instance(self) -> EmailService:
        return MagicMock()
