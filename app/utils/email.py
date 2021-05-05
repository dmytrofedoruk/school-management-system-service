from typing import List
from fastapi import BackgroundTasks
from pydantic import EmailStr, BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.config import Envs


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_USERNAME,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME
)


async def send_email(background_tasks: BackgroundTasks, email_to: str, body: str):
    try:
        message = MessageSchema(
            subject='Validate your account',
            recipients=[email_to],
            body=body,
            subtype='html'
        )

        fm = FastMail(conf)

        print('message', message)
        print('conf', conf)

        await fm.send_message(message)
    except Exception as error:
        print('error sending email', error)
