import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # ensure templates are auto_reloaded
    TEMPLATES_AUTO_RELOAD = True
    # configure session to use filesystem
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")


config_mode = {"development": DevelopmentConfig, "production": ProductionConfig}
