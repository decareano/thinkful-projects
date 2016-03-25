import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from tuneful.main import app
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
                "name": {"type" : "string"}
            },
            "required": ["id", "name"]
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
        "name": {"type", "string"}
    },
    "required": ["id", "name"]
}

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
    """ Returns list of all songs """
    songs = session.query(models.Song)
    songs = songs.order_by(models.Song.id)

    # Needs filtering.  

    data = json.dumps([songs.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

