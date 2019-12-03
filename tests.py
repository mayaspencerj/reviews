#!flask/bin/python
import os
import unittest

from app import app, db
from app.models import Accounts

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def unique_email(self):
        u = User(username='john', email='john@example.com', password="test")
        db.session.add(u)
        db.session.commit()
        email = User.unique_email('john@example.com')
        assert email != 'john@example.com'
        u = User(email=email, username='NotJohn')
        db.session.add(u)
        db.session.commit()
        email2 = User.unique_email('john@example.com')
        assert email2 != 'john@example.com'
        assert email2 != email

if __name__ == '__main__':
    unittest.main()
