#import libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#configuration and migration
app = Flask(__name__)
app.config.from_object('config_app')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

#import files from app folder
from app import views, models
