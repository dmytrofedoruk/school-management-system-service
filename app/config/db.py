import os
import sqlalchemy
from dotenv import load_dotenv
from databases import Database

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, '.env'))

db = Database(os.getenv('DATABASE_URL'))

metadata = sqlalchemy.MetaData()