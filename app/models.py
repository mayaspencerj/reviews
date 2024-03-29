from app import db
from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


AccountsCuisines = db.Table('AccountsCuisines', db.Model.metadata,
	db.Column('accounts_id', db.Integer, db.ForeignKey('accounts.id')),
	db.Column('cuisines_id', db.Integer, db.ForeignKey('cuisines.id'))
	)

#DECLARING MODEL, MY ITEMS TABLE TO HOLD TO DO ITEMS
class Accounts(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    items = db.relationship('Items', backref='accounts', lazy='dynamic')
    cuisines = db.relationship('Cuisines', secondary='AccountsCuisines', backref='Accounts', lazy='dynamic')


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(20), unique=False, nullable=False)
    content = db.Column(db.String(120), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location_long = db.Column(db.String(120), unique=False, nullable=True)
    location_lat = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

    def __init__(self,restaurant,content,location_long, location_lat,user_id):
        self.restaurant = restaurant
        self.content = content
        self.location_long = location_long
        self.location_lat = location_lat
        self.user_id = user_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""

        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)


class Cuisines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120), unique=False, nullable=True)


    def create_cuisines():
        cuisines = ['Italian','Indonesian','Turkish','Thai','Spanish','Moroccan','Japanese','Indian','French','Chinese']
        cuisines_ref = [1,2,3,4,5,6,7,8,9,10]
        for item in cuisines:
            for position in cuisines_ref:
                add_cuisine = AccountsCuisines(position, item)
                db.session.add(add_cuisine)
                db.session.commit()
