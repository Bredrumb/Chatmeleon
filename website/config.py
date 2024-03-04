from dotenv import load_dotenv
from pathlib import Path 
import os


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config: # Simply gets variables from .env file then exports as Config
    TESTING = os.getenv('TESTING')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER = os.getenv('SERVER')
