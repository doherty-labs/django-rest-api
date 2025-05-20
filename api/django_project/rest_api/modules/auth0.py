from unittest.mock import MagicMock

from django.conf import settings
from injector import Module, provider, singleton

from rest_api.services.auth0 import Auth0Init


class Auth0ServiceModule(Module):
    @provider
    def get_instance(self) -> Auth0Init:
        return Auth0Init(
            domain_host=settings.AUTH0_DOMAIN,
            rest_api_client_id=settings.AUTH0_REST_API_CLIENT_ID,
            rest_api_client_secret=settings.AUTH0_REST_API_CLIENT_SECRET,
            rest_api_audience=f"https://{settings.AUTH0_DOMAIN}/api/v2/",
        )


class TestAuth0ServiceModule(Module):
    @singleton
    @provider
    def get_instance(self) -> Auth0Init:
        mock = MagicMock()

        mock.get_org.return_value.create_organization.return_value = {
            "id": "org_123",
        }

        return mock
