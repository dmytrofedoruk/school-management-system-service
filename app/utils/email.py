import os
from typing import List
from fastapi import BackgroundTasks
from pydantic import EmailStr, BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.config import Envs
from app.config.config import BASE_DIR

conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    TEMPLATE_FOLDER=os.path.join(BASE_DIR, 'app', 'templates', 'email')
)


class BodyEmail(BaseModel):
    validation_url: str
    title: str
    h3: str
    p: str
    button_title: str


def send_email(background_tasks: BackgroundTasks, email_to: str, email_subject: str, body: BodyEmail):
    try:
        message = MessageSchema(
            subject=email_subject,
            recipients=[email_to],
            body={
                'validation_url': body.validation_url,
                'title': body.title,
                'p': body.p,
                'h3': body.h3,
                'button_title': body.button_title
            },
            subtype='html',
        )

        fm = FastMail(conf)

        background_tasks.add_task(
            fm.send_message, message, template_name='email.html')
    except Exception as error:
        return
