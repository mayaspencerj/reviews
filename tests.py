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
        db.session.remove()
        db.drop_all()

    def test_make_unique_nickname(self):
        u = Accounts(username='rebs', email='rebs@example.com',password="helpme")
        db.session.add(u)
        db.session.commit()
        nickname = Accounts.make_unique_nickname('rebs')
        assert nickname != 'rebs'
        u = Accounts(username=nickname, email='rebecca@example.com', password="helpme")
        db.session.add(u)
        db.session.commit()
        nickname2 = Accounts.make_unique_nickname('rebs')
        assert nickname2 != 'rebs'
        assert nickname2 != nickname
        
        
  
if __name__ == '__main__':
    unittest.main()
