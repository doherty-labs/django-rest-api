from datetime import datetime
from typing import Callable

from nylas import Client
from nylas.models.auth import CodeExchangeResponse
from nylas.models.contacts import Contact, ListContactsQueryParams
from nylas.models.drafts import SendMessageRequest

from django_project import settings


class NylasService:
    def __init__(self):
        self.nylas_client = Client(
            api_key=settings.NYLAS_CLIENT_SECRET, api_uri="https://api.eu.nylas.com"
        )

    def get_authenticate_url(
        self, email: str, merchant_id: int, redirect_uri: str
    ) -> str:
        return self.nylas_client.auth.url_for_oauth2(
            config={
                "client_id": settings.NYLAS_CLIENT_ID,
                "redirect_uri": redirect_uri,
                "login_hint": email,
                "access_type": "offline",
                "state": merchant_id,
            }
        )

    def exchange_code_for_token(
        self, code: str, redirect_uri: str
    ) -> CodeExchangeResponse:
        return self.nylas_client.auth.exchange_code_for_token(
            request={
                "client_id": settings.NYLAS_CLIENT_ID,
                "code": code,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }
        )

    def refresh_token(self, refresh_token: str) -> CodeExchangeResponse:
        return self.nylas_client.auth.refresh_access_token(
            request={
                "client_id": settings.NYLAS_CLIENT_ID,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            }
        )

    def get_all_contacts(
        self,
        grant_id: str,
        chunk_size: int,
        chunk_processor: Callable[[list[Contact], int], None],
        merchant_id: int,
    ) -> None:
        contacts = self.nylas_client.contacts.list(
            identifier=grant_id, query_params=ListContactsQueryParams(limit=chunk_size)
        )
        chunk_processor(contacts.data, merchant_id)
        current_cursor = contacts.next_cursor

        while current_cursor:
            next_contacts = self.nylas_client.contacts.list(
                identifier=grant_id,
                query_params=ListContactsQueryParams(
                    limit=chunk_size, page_token=contacts.next_cursor
                ),
            )
            chunk_processor(next_contacts.data, merchant_id)
            current_cursor = next_contacts.next_cursor

    def send_email(self, grant_id: str, data: SendMessageRequest):
        return self.nylas_client.messages.send(
            grant_id,
            data,
        )

    def get_message_by_id(self, grant_id: str, message_id: str):
        return self.nylas_client.messages.find(grant_id, message_id)

    def delete_event(self, grant_id: str, event_id: str, calendar_id: str):
        return self.nylas_client.events.destroy(
            grant_id, event_id, query_params={"calendar_id": calendar_id}
        )

    def get_busy(
        self, grant_id: str, calendar_id: str, start_time: datetime, end_time: datetime
    ):
        return self.nylas_client.events.list(
            grant_id,
            query_params={
                "calendar_id": calendar_id,
                "start": int(start_time.timestamp()),
                "end": int(end_time.timestamp()),
                "show_cancelled": False,
                "limit": 200,
            },
        ).data

    def cancel_access(self, grant_id: str):
        return self.nylas_client.grants.destroy(grant_id)

    def get_grant(self, grant_id: str):
        return self.nylas_client.grants.find(grant_id)
