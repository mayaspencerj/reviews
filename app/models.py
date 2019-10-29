from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login



#DECLARING MODEL, MY ITEMS TABLE TO HOLD TO DO ITEMS
class Accounts(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
#   posts = db.relationship('Items', backref='author', lazy=True)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(20), unique=False, nullable=False)
    content = db.Column(db.String(120), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location_long = db.Column(db.String(120), unique=False, nullable=True)
    location_lat = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

    def __init__(self,restaurant,content,location_long, location_lat):
        self.restaurant = restaurant
        self.content = content
        self.location_long = location_long
        self.location_lat = location_lat

