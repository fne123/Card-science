import asyncio
import logging
from email.message import EmailMessage
from typing import Iterable, Optional

import aiosmtplib

from ..core.config import get_settings

logger = logging.getLogger(__name__)


class EmailSender:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def send_email(
        self,
        subject: str,
        recipients: Iterable[str],
        html_body: str,
        text_body: Optional[str] = None,
    ) -> None:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = f"{self.settings.mail_from_name} <{self.settings.mail_sender}>"
        message["To"] = ", ".join(recipients)
        message.set_content(text_body or "")
        message.add_alternative(html_body, subtype="html")

        if not self.settings.mail_username or not self.settings.mail_password:
            logger.warning("Mail credentials missing. Email not sent but logged.")
            logger.info("Subject: %s\nBody: %s", subject, html_body)
            return

        await aiosmtplib.send(
            message,
            hostname=self.settings.mail_smtp_host,
            port=self.settings.mail_smtp_port,
            start_tls=self.settings.mail_use_tls,
            username=self.settings.mail_username,
            password=self.settings.mail_password,
        )

    def send_in_background(
        self,
        subject: str,
        recipients: Iterable[str],
        html_body: str,
        text_body: Optional[str] = None,
    ) -> None:
        asyncio.create_task(self.send_email(subject, recipients, html_body, text_body))


email_sender = EmailSender()
