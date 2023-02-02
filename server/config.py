from dotenv import load_dotenv
import os

load_dotenv()

TESTING = True
DEBUG = True
FLASK_ENV = 'development'

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

if DEBUG:
    TEMPLATES_AUTO_RELOAD = True

