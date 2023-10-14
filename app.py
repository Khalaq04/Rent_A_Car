from flask import Flask
from applications import config
from applications.config import LocalDevelopementConfig
from applications.database import db

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopementConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from applications.UtilsController import *

if __name__ == '__main__':
    app.run()