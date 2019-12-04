#!flask/bin/python
import os, sys
import unittest
basedir = os.path.abspath(os.path.dirname(__file__)) #obtains parent directory 
from app import app, db
from app.models import Accounts


class TestCase(unittest.TestCase):
    def test_setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def test_tearDown(self):
        pass
       # db.session.remove()
        #db.drop_all()


    def test_users_can_login(self):
        u = Accounts(username='Joe', email='joe@joes.com', password='12345')
        db.session.add(u)
        db.session.commit()


  
if __name__ == '__main__':
    unittest.main()
