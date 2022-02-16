import http
import os
import unittest
import json

import memoize as memoize
import requests as requests
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, User, Tag


class TagsTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = os.getenv('DATABASE_URL')
        setup_db(self.app, self.database_path)

        self.test_user = {
            "name": "Arturo Diaz",
            "telephone": "997207077"
        }

        self.test_tag = {
            "name": "Melkor",
            "information": "mixed race dog, medium size",
            "user_id": 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    get_users should respond only to admin,
    401 if no token present
    403 if token doesn't have the persmissions
    """

    def test_get_users(self):
        res = self.client().get('/users',
                                headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['users'])

    def test_get_users_401(self):
        res = self.client().get('/users')
        self.assertEqual(res.status_code, 401)

    def test_get_users_403(self):
        res = self.client().get('/users',
                                headers={'Authorization': "Bearer " + os.getenv('USER_TOKEN')})
        self.assertEqual(res.status_code, 403)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
