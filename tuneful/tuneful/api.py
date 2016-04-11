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
            "minLength": 1},
            "id": {"type": "number"}
    },
    "required": ["filename", "id"]
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

    # Check if song files are legit.  If not, delete them
    for song in songs:
        print(os.path.isfile(upload_path(song.file.filename)))
        if not os.path.isfile(upload_path(song.file.filename)):
            file = session.query(models.File).get(song.file.id)
            print("Deleting song id {} with file id {}".format(
                song.id, file.id))
            session.delete(song)
            session.delete(file)
            session.commit()

    # Needs filtering?  Doesn't really make sense from the schema, 
    # not enough properties to work with
    if not songs:
        message = "No songs in database."
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps([song.as_dictionary() for song in songs])
    # print(data)
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
@decorators.require("application/json")
def song_post():
    """ Post a new song, by posting a file object """
    data = request.json


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

@app.route("/api/songs/<int:id>", methods=["PUT"])
@decorators.accept("application/json")
@decorators.require("application/json")
def song_edit(id):
    """ PUT (edit) an existing song """
    data = request.json

    # Check if it's legit schema
    try:
        validate(data, file_POST_Schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    fileid = data["file"]["id"]

    # Check if song exists. Returns error if not found:
    song = session.query(models.Song).get(id)
    if not song:
        message = "Song with id {} not in database.".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Check if file exists. Returns error if not found:
    file = session.query(models.File).get(fileid)
    if not file:
        message = "File with id {} not in database.".format(fileid)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Edit song to point to new file
    try:
        song.file = file
        session.commit()
    except Exception as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    # Return a 200 Accepted, containing the song as JSON and with the
    # Location header set to the location of the song
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("song_get", id=song.id)}
    return Response(data, 200, headers=headers,
        mimetype="application/json")


@app.route("/api/songs/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def song_delete(id):
    """ DELETE an existing file, and song associated with it"""

    # Check if song exists. Returns error if not found:
    file = session.query(models.File).get(id)
    if not file:
        message = "File with id {} not in database.".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # DELETE songs with this file in the db.  Also delete the file.
    try:
        song = session.query(models.Song).get(id)
        session.delete(song)
        session.delete(file)
        session.commit()
    except Exception as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    # Return a 200 Accepted
    message = "Deleted file, and song pointing to file, with id {}".format(id)
    data = json.dumps({"message": message})
    return Response(data, 200, mimetype="application/json")

@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)

@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    file = request.files.get("file")
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    filename = secure_filename(file.filename)
    db_file = models.File(filename=filename)
    session.add(db_file)
    session.commit()
    file.save(upload_path(filename))

    data = db_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")