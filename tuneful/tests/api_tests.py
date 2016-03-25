import os
import shutil
import json
import unittest
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO

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



    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())


