from unittest.mock import MagicMock

from django.conf import settings
from injector import Module, provider, singleton
from mixpanel import Consumer, Mixpanel

from rest_api.services.mixpanel import MixpanelService


class MixpanelModule(Module):
    @singleton
    @provider
    def get_instance(self) -> MixpanelService:
        return MixpanelService(
            mxp=Mixpanel(
                settings.MIXPANEL_TOKEN,
                consumer=Consumer(api_host="api-eu.mixpanel.com"),
            ),
        )


class TestMixpanelModule(Module):
    @singleton
    @provider
    def get_instance(self) -> MixpanelService:
        return MagicMock()
