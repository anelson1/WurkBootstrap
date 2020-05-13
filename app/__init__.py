from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message


myapp = Flask(__name__)
myapp.config.from_object(Config)
db = SQLAlchemy(myapp)
migrate = Migrate(myapp, db)
login = LoginManager(myapp)
mail = Mail(myapp)
bootstrap = Bootstrap(myapp)


login.login_view = 'login'

from app import routes, database
