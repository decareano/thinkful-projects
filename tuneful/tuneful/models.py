import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

# from tuneful import app
from .database import Base, engine

class Song(Base):
    """ Song class scheme """
    __tablename__ = "song"
    id = Column(Integer, primary_key=True)
    file = relationship("File", uselist=False, backref="song")

    def as_dictionary(self):
        song = {
        "id": self.id,
        "file": {
            "id": self.file.id,
            "name": self.file.filename
            }
        }

class File(Base):
    """ File class scheme """
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)
    filename = Column(String(128), nullable=False)
    song_id = Column(Integer, ForeignKey('song.id'), nullable = False)
    # song = relationship("Song", back_populates="file")

    def as_dictionary(self):
        file = {
            "id": self.file.id,
            "name": self.file.filename
        }
