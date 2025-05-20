from django.conf import settings
from stripe import Account, Customer, StripeClient


class StripeService:
    def __init__(self) -> None:
        self.stripe_client = StripeClient(settings.STRIPE_API_KEY)

    def create_connect_account(self, email: str) -> Account:
        return self.stripe_client.accounts.create(
            params={"type": "standard", "email": email},
        )

    def retrieve_account(self, account_id: str) -> Account:
        return self.stripe_client.accounts.retrieve(account_id)

    def create_customer(self, name: str) -> Customer:
        return self.stripe_client.customers.create(params={"name": name})
