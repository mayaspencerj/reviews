#!flask/bin/python
import os, sys
import unittest
basedir = os.path.abspath(os.path.dirname(__file__)) #obtains parent directory 
from app import app, db, views
from app.models import Accounts


class TestCase(unittest.TestCase):
    def test_setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def test_tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_profile_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)
        self.assertIn(b'Account Actions', response.data)
        self.assertIn(b'Statistics', response.data)
        self.assertIn(b'First time logged in. Welcome!', response.data)
     
     

if __name__ == '__main__':
    unittest.main()
    
