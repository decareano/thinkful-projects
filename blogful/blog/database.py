from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from flask.ext.login import UserMixin

from blog import app


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from .database import Base, engine

class User(Base, UserMixin):
    """Users Table"""
    __tablename__ = "users"

    id =  Column(Integer, primary_key = True)
    name = Column(String(128))
    email = Column(String(128), unique = True)
    password = Column(String(10084))
    entries = relationship("Entry", backref="author")

class Entry(Base):
    """Entries Table"""
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))

    # for legacy entries, I used the following SQL to populate them with a dummy account:
    #
    # update entries set author_id=t.id from 
    # (select id as id from users where users.email='retro@active.com') t  
    # where entries.author_id is NULL;
    
Base.metadata.create_all(engine)
