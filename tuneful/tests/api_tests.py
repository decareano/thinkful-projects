import os
import shutil
import json
import unittest
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO, BytesIO

import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful.main import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session



class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def test_get_empty_songs(self):
        """ Getting posts from empty db """
        response = self.client.get("/api/songs",
                headers=[("Accept", "application/json")]
                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])

    def test_unsupported_accept_header(self):
        response = self.client.get("/api/songs",
            headers=[("Accept", "application/xml")]
            )

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["message"],
            "Request must accept application/json data")


        
    def test_get_song(self):
        """ Getting a single post from a populated db """
        fileA = models.File(filename="testA.wav")
        songA = models.Song(file=fileA)
        
        fileB = models.File(filename="testB.wav")
        songB = models.Song(file=fileB)

        session.add_all([fileA, fileB, songA, songB])
        session.commit()

        response = self.client.get("api/songs/{}".format(songB.id),
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        song = json.loads(response.data.decode("ascii"))
        self.assertEqual(song["file"]["filename"], "testB.wav")


    def test_post_file(self):
        fileA = models.File(filename="testA.wav")
        session.add(fileA)
        session.commit()

        fileA_post = {
        "file":{
            "id": fileA.id
            }
        }
        # data = fileA.as_dictionary()
        data = fileA_post


        response = self.client.post("api/songs",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(urlparse(response.headers.get("Location")).path,
                         "/api/songs/1")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["file"]["filename"], "testA.wav")

        songs = session.query(models.Song).all()
        self.assertEqual(len(songs), 1)

        song = songs[0]
        self.assertEqual(song.file.filename, "testA.wav")


    def test_invalid_data(self):
        """ Posting a song file with an invalid format """
        # NEEDS TO BE MORE GENERIC
        data = {
            "file": {
                "id": "pancakes"
                }
        }

        response = self.client.post("/api/songs",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 422)

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["message"], "'pancakes' is not of type 'number'")

    def test_post_absent_file(self):
        """ Posting a file not in db """
        data = {
            "file": {
                "id": 0
                }
        }

        response = self.client.post("/api/songs",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_file(self):
        fileA = models.File(filename="testA.wav")
        songA = models.Song(file=fileA)
        session.add_all([fileA, songA])
        session.commit()


        # 1st, see if song was successfully posted
        response = self.client.get("api/songs/{}".format(songA.id),
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        # Now test DELETE
        response = self.client.delete("/api/songs/{}".format(songA.id),
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        # Try GET to check if 404
        response = self.client.get("api/songs/{}".format(songA.id),
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, "application/json")

    def test_edit_song(self):
        fileA = models.File(filename="testA.wav")
        fileB = models.File(filename="testB.wav")
        song = models.Song(file=fileA)

        session.add_all([fileA, fileB, song])
        session.commit()

        newfile = {
        "file":{
            "id": fileB.id
            }
        }
        data = newfile

        response = self.client.get("api/songs/{}".format(song.id),
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        songjson = json.loads(response.data.decode("ascii"))
        self.assertEqual(songjson["file"]["filename"], "testA.wav")

        response = self.client.put("/api/songs/{}".format(song.id),
            data = json.dumps(data),
            content_type = "application/json",
            headers=[("Accept", "application/json")]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        songjson = json.loads(response.data.decode("ascii"))
        self.assertEqual(songjson["file"]["filename"], "testB.wav")
        self.assertEqual(songjson["file"]["id"], fileB.id)


    def test_get_uploaded_file(self):
        path =  upload_path("test.txt")
        with open(path, "wb") as f:
            f.write(b"File contents")

        response = self.client.get("/uploads/test.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/plain")
        self.assertEqual(response.data, b"File contents")

    def test_file_upload(self):
        data = {
            "file": (BytesIO(b"File contents"), "test.txt")
        }

        response = self.client.post("/api/files",
            data=data,
            content_type="multipart/form-data",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(urlparse(data["path"]).path, "/uploads/test.txt")

        path = upload_path("test.txt")
        self.assertTrue(os.path.isfile(path))
        with open(path, "rb") as f:
            contents = f.read()
        self.assertEqual(contents, b"File contents")


    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())


