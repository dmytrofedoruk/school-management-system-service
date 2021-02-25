from fastapi import FastAPI

from .accounts.routers import account_router

app = FastAPI()

app.include_router(account_router)


@app.get('/')
def root():
    return {'Welcome to school system application version: 0.0.1'}