from typing import Dict, List, Optional, Union

from fastapi import UploadFile
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.schemas.mail import EmailTemplates
from app.templates.context import get_template_context

from .config import Config
from .template_registry import TemplateRegistry

template_registry = TemplateRegistry()

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
    TEMPLATE_FOLDER=template_registry.TEMPLATES_DIR,
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


class MailerService:
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
        message = MailerService._create_message(
            recipients=[email],
            subject=EmailTemplates.EMAIL_VERIFICATION.subject,
            template_body=get_template_context(first_name=first_name, verification_url=verification_url),
        )

        await MailerService.mail.send_message(message=message, template_name=EmailTemplates.EMAIL_VERIFICATION.template)

    @staticmethod
    async def send_password_reset(email: str, first_name: str, reset_url: str):
        message = MailerService._create_message(
            recipients=[email],
            subject=EmailTemplates.PWD_RESET.subject,
            template_body=get_template_context(first_name=first_name, reset_url=reset_url),
        )

        await MailerService.mail.send_message(message=message, template_name=EmailTemplates.PWD_RESET.template)

    @staticmethod
    async def send_waitlist_confirmation(email: str, name: str):
        message = MailerService._create_message(
            recipients=[email],
            subject=EmailTemplates.WAITLIST_CONFIRMATION.subject,
            template_body=get_template_context(name=name),
        )

        await MailerService.mail.send_message(
            message=message, template_name=EmailTemplates.WAITLIST_CONFIRMATION.template
        )
