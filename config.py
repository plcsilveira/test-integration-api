import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///transportadora.db' # Define o arquivo do banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False