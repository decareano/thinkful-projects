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
                "filename": {"type" : "string"}
            },
            "required": ["filename"]
        }
    },

    "type": "object",

    "properties": {
        "file": {"$ref": "#/definitions/file"}
    },
    "required": ["file"]
}

file_schema = {
    "type": "object",
    "properties": {
            "filename": {"type": "string",
            "minLength": 1}
    },
    "required": ["filename"]
}

file_POST_Schema = {
    "definitions": {
        "file": {
            "type": "object",
            "properties": {
                "id": {"type" : "number"}
            },
            "required": ["id"]
        }
    },

    "type": "object",

    "properties": {
        "file": {"$ref": "#/definitions/file"}
    },
    "required": ["file"]
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
    """ Post a new song, by posting a file object """
    data = request.json
    # print(data)
    # print(data["file"]["id"])

    # Check if it's legit
    try:
        validate(data, file_POST_Schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    id = data["file"]["id"]

    # Check if song exists. Returns error if not found:
    file = session.query(models.File).get(id)
    if not file:
        message = "File with id {} not in database.".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Add song to the database
    try:
        song = models.Song(file=file)
        session.add(file, song)
        session.commit()
    except Exception as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")



    # Return a 201 Created, containing the song as JSON and with the
    # Location header set to the location of the song
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("song_get", id=song.id)}
    return Response(data, 201, headers=headers,
        mimetype="application/json")
