from pathlib import Path
from typing import Dict, List, Optional, Union

from fastapi import UploadFile
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from src.misc.schemas import EmailTypes

from .config import Config

ROOT_DIR = Path(__file__).resolve().parent.parent

mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=int(Config.MAIL_PORT),
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_STARTTLS=Config.MAIL_STARTTLS in [True, "True", "true", 1, "1"],
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS in [True, "True", "true", 1, "1"],
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(ROOT_DIR, "templates"),
)

mail = FastMail(config=mail_config)


def create_message(
    recipients: List[EmailStr],
    attachments: List[Union[UploadFile, Dict, str]] = [],
    subject: str = "",
    body: Optional[Union[List, str]] = None,
    template_body: Optional[Union[List, str]] = None,
) -> MessageSchema:
    message = MessageSchema(
        recipients=recipients,
        attachments=attachments,
        subject=subject,
        body=body,
        template_body=template_body,
        subtype=MessageType.html,
    )

    return message


class Mailer:
    mail = FastMail(config=mail_config)

    @staticmethod
    def _create_message(
        recipients: List[EmailStr],
        attachments: List[Union[UploadFile, Dict, str]] = [],
        subject: str = "",
        body: Optional[Union[List, str]] = None,
        template_body: Optional[Union[List, str]] = None,
    ) -> MessageSchema:
        message = MessageSchema(
            recipients=recipients,
            attachments=attachments,
            subject=subject,
            body=body,
            template_body=template_body,
            subtype=MessageType.html,
        )

        return message

    @staticmethod
    async def send_email_verification(email: str, first_name: str, verification_url: str):
        message = Mailer._create_message(
            recipients=[email],
            subject=EmailTypes.EMAIL_VERIFICATION.subject,
            template_body={"first_name": first_name, "verification_url": verification_url},
        )

        await Mailer.mail.send_message(message=message, template_name=EmailTypes.EMAIL_VERIFICATION.template)

    @staticmethod
    async def send_password_reset(email: str, first_name: str, reset_url: str):
        message = Mailer._create_message(
            recipients=[email],
            subject=EmailTypes.PWD_RESET.subject,
            template_body={"first_name": first_name, "reset_url": reset_url},
        )

        await Mailer.mail.send_message(message=message, template_name=EmailTypes.PWD_RESET.template)
