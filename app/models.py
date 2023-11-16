from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey
from sqlalchemy_utils import URLType
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Define User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)


# Define Game model
class Game(Base):
    __tablename__ = "games"
    game_id = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    review = Column(Text)
    photo = Column(URLType)
    own_it = Column(Boolean, nullable=False)
    rating = Column(Integer, nullable=False)
    price = Column(Integer)
    date = Column(Date)


# Define Site model
class Site(Base):
    __tablename__ = "sites"
    site_id = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(URLType, nullable=False)


# Define DefaultSite model
class DefaultSite(Base):
    __tablename__ = "default_sites"
    site_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(URLType, nullable=False)
