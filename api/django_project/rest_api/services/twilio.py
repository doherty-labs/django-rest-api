from twilio.rest import Client

from django_project import settings


class SMSNotificationService:
    def get_twilio_client(self):
        return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_sms(self, to: str, body: str, phone_number: str):
        return self.get_twilio_client().messages.create(
            to=to, from_=phone_number, body=body
        )
