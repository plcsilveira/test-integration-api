import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///transportadora.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VALOR_FIXO_FRETE = float(os.getenv('VALOR_FIXO_FRETE', 10.0))