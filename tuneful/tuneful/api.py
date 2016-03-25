import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from .main import app
from .database import session
from .utils import upload_path


# Learned from 
# https://spacetelescope.github.io/understanding-json-schema/structuring.html#structuring
song_schema = {
    "definitions": {
        "file": {
            "type": "object",
            "properties": {
                "id": {"type" : "number"},
                "filename": {"type" : "string"}
            },
            "required": ["id", "filename"]
        }
    },

    "type": "object",

    "properties": {
        "id": {"type" : "number"},
        "file": {"$ref": "#/definitions/file"}
    },
    "required": ["id", "file"]
}

file_schema = {
    "type": "object",
    "properties": {
        "id": {"type", "number"},
        "filename": {"type", "string"}
    },
    "required": ["id", "filename"]
}

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
    """ Returns list of songs """
    songs = session.query(models.Song)
    songs = songs.order_by(models.Song.id)

    # Needs filtering?  Doesn't really make sense from the schema, 
    # not enough properties to work with

    data = json.dumps([songs.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/songs/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def song_get(id):
    """ Returns single song """
    song = session.query(models.Song).get(id)

    # Check for song's existence
    if not song:
        message = "Could not find song with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps(song.as_dictionary())
    return Response(data, 200, mimetype="application/json")

@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
def song_post():
    pass
