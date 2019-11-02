#import libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt





#configuration and migration
app = Flask(__name__)
app.config.from_object('config_app')
login_man = LoginManager()
login_man.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)






#import files from app folder
from app import views, models
