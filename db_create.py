from config_app import SQLALCHEMY_DATABASE_URI

from app import db
import os.path

# Creates the table and the database
db.create_all()

