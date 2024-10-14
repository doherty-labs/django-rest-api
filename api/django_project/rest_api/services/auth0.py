from urllib.parse import urlsplit

from auth0.v3.authentication import Database
from auth0.v3.authentication.get_token import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management.organizations import Organizations
from auth0.v3.management.users import Users
from auth0.v3.management.users_by_email import UsersByEmail

from django_project import settings


class Auth0Service:

    domain = settings.AUTH0_DOMAIN
    domain_host = urlsplit(domain).hostname

    rest_api_client_id = settings.AUTH0_REST_API_CLIENT_ID
    rest_api_client_secret = settings.AUTH0_REST_API_CLIENT_SECRET
    rest_api_audience = "https://{}/api/v2/".format(domain_host)

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
                        },
                        {
                            "connection_id": settings.AUTH0_GOOGLE_CONNECTION_ID,
                            "assign_membership_on_login": False,
                        },
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

    def signup_consumer(self, email: str, password: str) -> str:
        user_id: str = ""
        try:
            signup_req = self.get_database().signup(
                email=email,
                password=password,
                connection="Username-Password-Authentication",
                client_id=settings.AUTH0_STOREFRONT_APP_CLIENT_ID,
            )
            user_id = "auth0|" + signup_req.get("_id")
            self.get_database().change_password(
                client_id=settings.AUTH0_STOREFRONT_APP_CLIENT_ID,
                connection="Username-Password-Authentication",
                email=email,
            )
        except Auth0Error:
            user_id = (
                self.get_users_by_email()
                .search_users_by_email(email=email)[0]
                .get("user_id")
            )

        user_id = user_id.replace("|", "auth0.")
        return user_id

    def delete_user(self, user_id: str):
        return self.get_users().delete(user_id)

    def delete_org(self, id: str):
        return self.get_org().delete_organization(id)

    def assign_consumer_role(self, id: str):
        user_id = id.replace(".", "|")
        return self.get_users().add_roles(user_id, [settings.AUTH0_CUSTOMER_ROLE_ID])

    def assign_merchant_role(self, id: str):
        user_id = id.replace(".", "|")
        return self.get_users().add_roles(user_id, [settings.AUTH0_MERCHANT_ROLE_ID])
