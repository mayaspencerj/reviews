#!flask/bin/python
import os, sys
import unittest
basedir = os.path.abspath(os.path.dirname(__file__)) #obtains parent directory
from app import app, db
from app.models import Accounts
import bcrypt


class TestCase(unittest.TestCase):
    #set up unit testing and create db
    def test_setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        #SET UP FOR ACCOUNTS TESTING
        self.username = "Amy"
        self.username2 = "Aimee"
        self.int_username = 7
        self.longer_username = "AmyUsernameIsLongerThan30Characters"
        self.email = 'amy@leeds.ac.uk'
        self.email2 = "aimee@leeds.ac.uk"
        self.string_email = "amynotrealemail"
        self.int_email = 99
        self.longer_email = "Amyhasareallyreallyreallyreallylongemail@googlemail.co.uk"
        self.password = 'testing'
        self.longer_password = 'testingtestingtestingtestingtestingtestingtesting'
        self.u = Accounts(username=self.username, email=self.email, password=self.password)
        self.u2 = Accounts(username=self.username, email=self.email2, password=self.password)
        self.u3 = Accounts(username=self.username2, email=self.email2, password=self.password)
        self.account_longer_username = Accounts(username=self.longer_username, email=self.email, password=self.password)
        self.account_longer_email = Accounts(username=self.username, email=self.longer_email, password=self.password)
        self.account_longer_password = Accounts(username=self.username, email=self.email, password=self.longer_password)
        self.account_int_email = Accounts(username=self.username, email=self.int_email, password=self.password)
        self.account_int_username = Accounts(username=self.int_username, email=self.email, password=self.password)
        self.account_str_email = Accounts(username=self.username, email=self.string_email, password=self.password)

        self.no_password = Accounts(username=self.username, email=self.email)
        self.no_email = Accounts(username=self.username, password = self.password)
        self.no_username = Accounts(username=self.username, email=self.email)


    

    #delete all records in db
    def test_tearDown(self):
        Accounts.query.delete()
        pass

    #test duplicate usernames cannot be used and expect commit to fail
    @unittest.expectedFailure
    def test_register_username(self):
        db.session.add(self.u)
        db.session.add(self.u2)
        db.session.commit()
        self.assertTrue(False)

    #test duplicate emails cannot be used and expect commit to fail
    @unittest.expectedFailure
    def test_register_email(self):
        db.session.add(self.u2)
        db.session.add(self.u3)
        db.session.commit()
        self.assertTrue(False)

    #test username length cannot exceed: 30 characters
    @unittest.expectedFailure
    def test_max_username_length(self):
        db.session.add(self.account_longer_username)
        db.session.commit()
        self.assertTrue(False)

    #test email length cannot exceed: 120 characters
    @unittest.expectedFailure
    def test_max_email_length(self):
        db.session.add(self.account_longer_email)
        db.session.commit()
        self.assertTrue(False)

    #test password length cannot exceed: 60 characters
    @unittest.expectedFailure
    def test_max_password_length(self):
        db.session.add(self.account_longer_password)
        db.session.commit()
        self.assertTrue(False)

    #test email field cannot be blank
    @unittest.expectedFailure
    def test_no_email(self):
        db.session.add(self.no_email)
        db.session.commit()
        self.assertTrue(False)

    #test password field cannot be blank
    @unittest.expectedFailure
    def test_no_password(self):
        db.session.add(self.no_password)
        db.session.commit()
        self.assertTrue(False)

    #test username field cannot be blank
    @unittest.expectedFailure
    def test_no_username(self):
        db.session.add(self.no_username)
        db.session.commit()
        self.assertTrue(False)

    #test username field cannot be an integer
    @unittest.expectedFailure
    def test_username_integer(self):
        db.session.add(self.account_int_username)
        db.session.commit()
        self.assertTrue(False)

    #test email field cannot be an integer
    @unittest.expectedFailure
    def test_email_integer(self):
        db.session.add(self.account_int_email)
        db.session.commit()
        self.assertTrue(False)

    #test email field cannot be a string
    @unittest.expectedFailure
    def test_email_string(self):
        db.session.add(self.account_string_email)
        db.session.commit()
        self.assertTrue(False)




if __name__ == '__main__':
    unittest.main()
