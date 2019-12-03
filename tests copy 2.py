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

    def test_change_password_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('pat','patkennedy79@gmail.com','passwordworks')
        response = self.app.get('/password_change')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password Change', response.data)
     
    def test_change_password(self):
        self.app.get('/register', follow_redirects=True)
        self.register('pat','patkennedy79@gmail.com','passwordworks')
        response = self.app.post('/user_password_change', data=dict(password='MyNewPassword1234'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password has been updated!', response.data)
        self.assertIn(b'User Profile', response.data)

        
        
  
if __name__ == '__main__':
    unittest.main()
    
