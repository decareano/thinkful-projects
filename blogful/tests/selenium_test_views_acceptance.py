import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
# from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# Configure app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test Setup """
        # If running on a server w/o desktop support, install and use
        # Xvfb to create a headless version of Firefox.
        # http://scraping.pro/use-headless-firefox-scraping-linux/
        # self.browser = Browser("firefox")
        firefoxProfile = webdriver.FirefoxProfile()
        self.browser = webdriver.Firefox(firefoxProfile)

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = User(name="Alice", email="alice@example.com",
            password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        # integrityError?  Try re-syncing primary key fields:
        # SELECT setval('tablename_id_seq', (SELECT MAX(id) FROM tablename)+1)

        # NOTE learn more about 'multiprocessing'.  Can run/control
        # other code simultaneously. 
        self.process = multiprocessing.Process(target=app.run,
            kwargs={"port": 8080})

        self.process.start()
        time.sleep(3)

    def test_login_correct(self):
        # Splinter
        # self.browser.visit("http://127.0.0.1:8080/login")
        # self.browser.fill("email", "alice@example.com")
        # sekf.browser.fill("password", "test")
        # button = self.browser.find_by_css("button[type=submit]")
        # button.click
        # self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")

        # Selenium
        self.browser.get("http://127.0.0.1:8080/login")
        loginElem = self.browser.find_element_by_id("email")
        loginElem.send_keys("alice@example.com")
        passElem = self.browser.find_element_by_id("password")
        passElem.send_keys("test")
        passElem.submit()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")

    # def test_login_incorrect(self):
    #     self.browser.visit("http://127.0.0.1:8080/login")
    #     self.browser.fill("email", "bob@example.com")
    #     self.browser.fill("password", "test")
    #     button = self.browser.find_by_css("button[type=submit]")
    #     button.click()
    #     self.assertEqual(self.browser.url, "http://127.0.0.1:8080/login")

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()