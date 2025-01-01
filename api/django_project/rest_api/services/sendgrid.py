import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

from django_project import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self) -> None:
        self.sendgrid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    def send_email(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        content: str,
    ) -> None:
        message = Mail(
            from_email=from_email,
            to_emails=[To(to_email)],
            subject=subject,
            html_content=content,
        )

        try:
            self.sendgrid_client.send(message)
        except Exception:
            msg = f"Failed to send email to {to_email}"
            logger.exception(msg)
            raise
