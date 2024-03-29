from flask import Flask

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.app_context().push()
    return app

app = create_app()

from applications.UtilsController import *
from applications.DriverController import *
from applications.CustomerController import *
from applications.EmployeeController import *
from applications.AdminController import *

if __name__ == '__main__':
    app.run(debug=True)