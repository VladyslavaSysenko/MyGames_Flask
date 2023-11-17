from flask import Flask
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv
import os
import sys

# Create parent directory main
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from config import config_mode

load_dotenv()


# configure application
app = Flask(__name__)
app.config.from_object(config_mode[os.getenv("CONFIG_MODE")])

Session(app)
# configure SQLAlchemy
DATABASE_URL = app.config["SQLALCHEMY_DATABASE_URI"]
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


# create tables
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    from urls import bp

    app.register_blueprint(bp)
    app.run(host="0.0.0.0")
