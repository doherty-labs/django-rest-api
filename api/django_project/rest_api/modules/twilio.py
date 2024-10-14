from unittest.mock import MagicMock

from injector import Module, provider, singleton

from rest_api.services.twilio import SMSNotificationService


class SMSModule(Module):
    @singleton
    @provider
    def get_instance(self) -> SMSNotificationService:
        return SMSNotificationService()


class TestSMSModule(Module):
    @singleton
    @provider
    def get_instance(self) -> SMSNotificationService:
        return MagicMock()
