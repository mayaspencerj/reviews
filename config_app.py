import os
basedir = os.path.abspath(os.path.dirname(__file__))

#SET THE PATHWAY OF THE DB FILE, MIGRATION FILE AND SECRET KEY
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'site.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_migrations')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '234iujvec984c839mji'


