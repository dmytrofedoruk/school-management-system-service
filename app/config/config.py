import os, sys
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, '.env.dev'))
sys.path.append(BASE_DIR)

class Envs:
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv('ACCESS_TOKEN_EXPIRE_HOURS'))