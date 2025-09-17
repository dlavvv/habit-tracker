from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config) # applies the configuraions made in config.py

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login' # name of login route
login_manager.init_app(app)

from app.models import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

from app import routes, models