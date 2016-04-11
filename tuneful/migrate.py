from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from .database import Base
from .main import app

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()