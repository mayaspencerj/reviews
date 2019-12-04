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
        pass


    def test_users_can_login(self):
        u = Accounts(username='Joe', email='joe@joes.com', password='12345')
        db.session.add(u)
        db.session.commit()

        with self.test_client:
            response = self.client.post("/login", data={"username": "Joe", "password": "12345"})
            self.assert_redirects(response, url_for("view_all"))
            self.assertTrue(current_user.name == "Joe")
            self.assertFalse(current_user.is_anonymous())

            
       # response = self.client.post(url_for('login'),
                                  #  data={'email': 'joe@joes.com', 'password': '12345'})

        #self.assert_redirects(response, url_for('view_all'))


  
if __name__ == '__main__':
    unittest.main()
