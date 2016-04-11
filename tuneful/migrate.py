# NOTE: After running migrate.py db init, go to migrations/env.py and changed
# line 22 to :
# current_app.config.get('DATABASE_URI').replace("%", "%%"))
# in order to use correct URI variable for this project and % signs escaped with %%

from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from tuneful.main import app
from tuneful.database import Base

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata
        

manager = Manager(app)
migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()