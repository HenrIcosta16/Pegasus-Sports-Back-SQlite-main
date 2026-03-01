# import os

# class Config:
#     # Aqui você usa o banco PostgreSQL, substitua os valores conforme necessário
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://pegasus:pegasus123@localhost:5432/pegasusbase")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "your_secret_key"

# config.py
import os

class Config:
    # Usando SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pegasus.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Configurações adicionais
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000