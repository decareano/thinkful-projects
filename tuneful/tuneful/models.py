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
    # file = relationship("File", uselist=False, backref="song")
    file_id = Column(Integer, ForeignKey('file.id'))

    def as_dictionary(self):
        song = {
        "id": self.id,
        "file": {
            "id": self.file.id,
            "filename": self.file.filename,
            "path": url_for("uploaded_file", filename=self.file.filename)
            }
        }
        return song

class File(Base):
    """ File class scheme """
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)
    filename = Column(String(128), nullable=False)
    song = relationship("Song", uselist=False, backref="file")
    # song_id = Column(Integer, ForeignKey('song.id'))

    def as_dictionary(self):
        file = {
            "id": self.id,
            "filename": self.filename,
            "path": url_for("uploaded_file", filename=self.filename)
        }
        return file
