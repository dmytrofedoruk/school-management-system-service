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


def send_email(background_tasks: BackgroundTasks, email_to: str, body: str):
    try:
        message = MessageSchema(
            subject='Validate your account',
            recipients=[email_to],
            body={
                'name': 'Saskia Nurul Azhima'
            },
            subtype='html',
        )

        fm = FastMail(conf)

        background_tasks.add_task(
            fm.send_message, message, template_name='email.html')
    except Exception as error:
        return
