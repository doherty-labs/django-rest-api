from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance

from django_project import settings


class SMSNotificationService:
    def get_twilio_client(self) -> Client:
        return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_sms(self, to: str, body: str, phone_number: str) -> MessageInstance:
        return self.get_twilio_client().messages.create(
            to=to,
            from_=phone_number,
            body=body,
        )
