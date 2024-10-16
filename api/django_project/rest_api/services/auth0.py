from urllib.parse import urlsplit

from auth0.v3.authentication import Database
from auth0.v3.authentication.get_token import GetToken
from auth0.v3.management.organizations import Organizations
from auth0.v3.management.users import Users
from auth0.v3.management.users_by_email import UsersByEmail

from django_project import settings


class Auth0Service:

    domain = settings.AUTH0_DOMAIN
    domain_host = urlsplit(domain).hostname

    rest_api_client_id = settings.AUTH0_REST_API_CLIENT_ID
    rest_api_client_secret = settings.AUTH0_REST_API_CLIENT_SECRET
    rest_api_audience = f"https://{domain_host}/api/v2/"

    def get_token(self) -> GetToken:
        return GetToken(domain=self.domain_host)

    def access_token(self) -> str:
        return self.get_token().client_credentials(
            client_id=self.rest_api_client_id,
            client_secret=self.rest_api_client_secret,
            audience=self.rest_api_audience,
        )["access_token"]

    def get_org(self):
        access_token = self.access_token()
        return Organizations(domain=self.domain_host, token=access_token)

    def get_users(self):
        access_token = self.access_token()
        return Users(domain=self.domain_host, token=access_token)

    def get_database(self):
        return Database(domain=self.domain_host)

    def get_users_by_email(self):
        access_token = self.access_token()
        return UsersByEmail(domain=self.domain_host, token=access_token)

    def add_org(self, org_name: str, slug: str) -> str:
        return (
            self.get_org()
            .create_organization(
                {
                    "name": slug,
                    "display_name": org_name,
                    "enabled_connections": [
                        {
                            "connection_id": settings.AUTH0_DATABASE_CONNECTION_ID,
                            "assign_membership_on_login": False,
                        }
                    ],
                }
            )
            .get("id")
        )

    def add_org_user(self, org_id: str, auth0_user_id: str, roles: list[str] = []):
        self.get_org().create_organization_members(
            org_id,
            {"members": [auth0_user_id]},
        )

        if roles:
            self.get_users().add_roles(auth0_user_id, roles)

    def delete_user(self, user_id: str):
        return self.get_users().delete(user_id)

    def delete_org(self, id: str):
        return self.get_org().delete_organization(id)
