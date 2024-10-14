from unittest.mock import MagicMock

from injector import Module, provider, singleton

from rest_api.services.auth0 import Auth0Service


class TestAuth0Module(Module):
    @singleton
    @provider
    def get_instance(self) -> Auth0Service:
        mock = MagicMock()
        mock.add_org.return_value = "dsfsdf"
        return mock
