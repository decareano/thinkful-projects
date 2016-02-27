import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from blog import app
from blog.database import session, Entry, Base
from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.database import User
from blog.config import DevelopmentConfig

manager = Manager(app)
develcfg = DevelopmentConfig()
SERVER_IP = develcfg.SERVER_IP

class DB(object):
    """Database metadata object"""
    def __init__(self, metadata):
        super(DB, self).__init__()
        self.metadata = metadata


# Need to find a way to format the postgresql connection string to have two % signs wherever there is one
# Answer: edit it in ./migrations/env.py
migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    for i in range(25):
        entry = Entry(
            title="Test Entry #{}".format(i),
            content=content
        )
        session.add(entry)
    session.commit()

@manager.command
def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email already exists.")
        return
    password = ""

    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter Password: ")

    user = User(name=name, 
        email=email, 
        password = generate_password_hash(password, 
        method="pbkdf2:sha256",
        salt_length=10000))
    session.add(user)
    session.commit()

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host=SERVER_IP, port=port)

if __name__ == '__main__':
    manager.run()