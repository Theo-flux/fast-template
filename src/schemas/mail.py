from typing import List

from fastapi import UploadFile
from pydantic import BaseModel


class EmailType:
    def __init__(self, _subject: str, _template: str):
        self.subject = _subject
        self.template = _template


class EmailTypes:
    EMAIL_VERIFICATION = EmailType("Verify your account", "email_verification.html")
    PWD_RESET = EmailType("Password reset", "pwd_reset.html")


class EmailModel(BaseModel):
    subject: str
    reciepients: List[str]
    payload: dict
    template: str
    attachments: List[UploadFile] = ([],)
