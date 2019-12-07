#!flask/bin/python
import os, sys
import unittest
basedir = os.path.abspath(os.path.dirname(__file__)) #obtains parent directory
from app import app, db
from app.models import Items,Accounts
import bcrypt
from datetime import datetime
from sqlalchemy import Date

class TestCase(unittest.TestCase):
    #set up unit testing and create db
    def test_setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        #SET UP FOR REVIEWS TESTING

        self.content = 'Food was very spicy! Check with the waitress how spicy your dish is beforehand!'
        self.content2 = 'Great cheesy fries'
        self.restaurant = "mexican diner"
        self.restaurant2 = 'Five Guys in Leeds'
        self.length_checks = 'LengthCheckForAllDifferentFieldsInItemsTable'
        self.int_checks = 33
        self.both_cords = '-1.346'
        self.userID = 1
        self.basic_post = Items(restaurant=self.restaurant, content=self.content,location_lat=self.both_cords, location_long=self.both_cords, user_id=self.userID)
        self.post_no_rest = Items(restaurant=None, content=self.content, location_lat=self.both_cords, location_long=self.both_cords, user_id=self.userID)
        self.post_no_content = Items(restaurant=self.restaurant, content=None, location_lat=self.both_cords, location_long=self.both_cords, user_id=self.userID)
        self.post_no_cords = Items(restaurant=self.restaurant, content=self.content, location_lat=None, location_long=None, user_id=self.userID)
        self.post_no_userid= Items(restaurant=self.restaurant, content=self.content, location_lat=self.both_cords, location_long=self.both_cords,user_id=None)
        self.post_content = Items(restaurant=self.restaurant, content=self.content2,location_lat=self.both_cords, location_long=self.both_cords, user_id=self.userID)
        self.post_length_rest = Items(restaurant=self.length_checks, content=self.content,location_lat=self.both_cords, location_long=self.both_cords, user_id=self.userID)
        self.post_length_location =Items(restaurant=self.restaurant, content=self.content,location_lat=self.length_checks, location_long=self.length_checks, user_id=self.userID)
        self.post_length_content = Items(restaurant=self.restaurant, content=self.length_checks,location_lat=self.both_cords, location_long=self.both_cords, user_id=self.userID)
        self.post_int_rest = Items(restaurant=self.length_checks, content=self.content,location_lat=self.both_cords, location_long=self.both_cords, user_id=self.userID)
        self.post_int_location =Items(restaurant=self.restaurant, content=self.content,location_lat=self.int_checks, location_long=self.int_checks, user_id=self.userID)
        self.post_int_content = Items(restaurant=self.restaurant, content=self.int_checks,location_lat=self.both_cords, location_long=self.both_cords, user_id=self.userID)


    #delete all records in db
    def test_tearDown(self):
        Items.query.delete()
        pass

    #test restaurant cannot be null
    @unittest.expectedFailure
    def test_null_restaurant(self):
        db.session.add(self.post_no_rest)
        db.session.commit()
        self.assertTrue(False)

    #test content cannot be null
    @unittest.expectedFailure
    def test_null_content(self):
        db.session.add(self.post_no_content)
        db.session.commit()
        self.assertTrue(False)


    #test content cannot be duplicated
    @unittest.expectedFailure
    def test_duplicate_content(self):
        db.session.add(self.basic_post)
        db.session.add(self.post_content)
        db.session.commit()
        self.assertTrue(False)

    #test user_id cannot be null
    @unittest.expectedFailure
    def test_null_userid(self):
        db.session.add(self.post_no_userid)
        db.session.commit()
        self.assertTrue(False)

    #test restaurant cannot exceed 20 characters
    @unittest.expectedFailure
    def test_length_rest(self):
        db.session.add(self.post_length_rest)
        db.session.commit()
        self.assertTrue(False)

    #test content cannot exceed 120 characters
    @unittest.expectedFailure
    def test_length_content(self):
        db.session.add(self.post_length_content)
        db.session.commit()
        self.assertTrue(False)


    #test location fields cannot exceed 120 characters
    @unittest.expectedFailure
    def test_length_location(self):
        db.session.add(self.post_length_location)
        db.session.commit()
        self.assertTrue(False)


    #test restaurant cannot be an integer
    @unittest.expectedFailure
    def test_int_rest(self):
        db.session.add(self.post_int_rest)
        db.session.commit()
        self.assertTrue(False)

    #test content cannot be an integer
    @unittest.expectedFailure
    def test_int_content(self):
        db.session.add(self.post_int_content)
        db.session.commit()
        self.assertTrue(False)

    #test location fields cannot be an integer
    @unittest.expectedFailure
    def test_int_location(self):
        db.session.add(self.post_int_location)
        db.session.commit()
        self.assertTrue(False)
















if __name__ == '__main__':
    unittest.main()
