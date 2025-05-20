from auth0.authentication import Database
from auth0.authentication.get_token import GetToken
from auth0.management.organizations import Organizations
from auth0.management.users import Users
from auth0.management.users_by_email import UsersByEmail
from django.conf import settings
from injector import inject


class Auth0Init:
    def __init__(
        self,
        domain_host: str,
        rest_api_client_id: str,
        rest_api_client_secret: str,
        rest_api_audience: str,
    ) -> None:
        self.domain_host = domain_host
        self.rest_api_client_id = rest_api_client_id
        self.rest_api_client_secret = rest_api_client_secret
        self.rest_api_audience = rest_api_audience

    def get_token(self) -> GetToken:
        return GetToken(
            domain=self.domain_host,
            client_id=self.rest_api_client_id,
            client_secret=self.rest_api_client_secret,
        )

    def access_token(self) -> str:
        return self.get_token().client_credentials(
            audience=self.rest_api_audience,
        )["access_token"]

    def get_org(self) -> Organizations:
        access_token = self.access_token()
        return Organizations(domain=self.domain_host, token=access_token)

    def get_users(self) -> Users:
        access_token = self.access_token()
        return Users(domain=self.domain_host, token=access_token)

    def get_database(self) -> Database:
        return Database(domain=self.domain_host)

    def get_users_by_email(self) -> UsersByEmail:
        access_token = self.access_token()
        return UsersByEmail(domain=self.domain_host, token=access_token)


class Auth0Service:
    @inject
    def __init__(self, auth0_init: Auth0Init) -> None:
        self.auth0_init = auth0_init

    def add_org(self, org_name: str, slug: str) -> str:
        return (
            self.auth0_init.get_org()
            .create_organization(
                {
                    "name": slug,
                    "display_name": org_name,
                    "enabled_connections": [
                        {
                            "connection_id": settings.AUTH0_DATABASE_CONNECTION_ID,
                            "assign_membership_on_login": False,
                        },
                        {
                            "connection_id": settings.AUTH0_GOOGLE_CONNECTION_ID,
                            "assign_membership_on_login": False,
                        },
                    ],
                },
            )
            .get("id")
        )

    def add_org_user(
        self,
        org_id: str,
        auth0_user_id: str,
        roles: list[str],
    ) -> None:
        self.auth0_init.get_org().create_organization_members(
            org_id,
            {"members": [auth0_user_id]},
        )

        if roles:
            self.auth0_init.get_users().add_roles(auth0_user_id, roles)

    def delete_user(self, user_id: str) -> None:
        self.auth0_init.get_users().delete(user_id)

    def delete_org(self, org_id: str) -> None:
        self.auth0_init.get_org().delete_organization(org_id)

    def assign_merchant_role(self, user_id: str) -> None:
        user_id_transformed = user_id.replace(".", "|")
        self.auth0_init.get_users().add_roles(
            user_id_transformed,
            [settings.AUTH0_MERCHANT_ROLE_ID],
        )
