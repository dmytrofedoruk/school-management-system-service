import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.db import db
from app.config.config import Envs
from app.routers import account_router, \
    classroom_router, \
    departement_router, \
    faculties_router


# Application instantiation
app = FastAPI(title='School System Management Service')

origins = [
    'http://localhost:8080',
    'http://0.0.0.0:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Seteup database connection and termination


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()

# Registering routers
app.include_router(account_router)
app.include_router(classroom_router)
app.include_router(departement_router)
app.include_router(faculties_router)


# Root path operation function
@app.get('/')
def root():
    return 'Welcome to school system application version: 0.0.1'

# running the service from manage.py file


def run():
    uvicorn.run('app.main:app', host=Envs.HOST, port=Envs.PORT,
                reload=True if Envs.ENVIRONMENT == 'development' else False)
