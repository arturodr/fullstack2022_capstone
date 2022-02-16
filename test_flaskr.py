import os
import unittest
import json

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

        self.test_patch_tag = {
            "information": "mixed race dog, big size"
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
    403 if token doesn't have the permissions
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

    """
    create_user should respond only to admin,
    401 if no token present
    403 if token doesn't have the permissions
    """

    def test_create_user(self):
        users_before_insert = User.total_users()

        response = self.client().post('/users',
                                      json=self.test_user,
                                      headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        data = json.loads(response.data)

        users_after_insert = User.total_users()

        self.assertTrue(users_after_insert - users_before_insert == 1)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_create_user_401(self):
        res = self.client().post('/users')
        self.assertEqual(res.status_code, 401)

    def test_create_user_403(self):
        res = self.client().post('/users',
                                 json=self.test_user,
                                 headers={'Authorization': "Bearer " + os.getenv('USER_TOKEN')})
        self.assertEqual(res.status_code, 403)

    """
    get_user_by_id should respond only to admin,
    401 if no token present
    403 if token doesn't have the permissions
    404 if the id doesn't exists
    """

    def test_get_user_by_id(self):
        res = self.client().get('/users/1',
                                headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['user'])

    def test_get_user_by_id_401(self):
        res = self.client().get('/users/1')
        self.assertEqual(res.status_code, 401)

    def test_get_user_by_id_403(self):
        res = self.client().get('/users/1',
                                headers={'Authorization': "Bearer " + os.getenv('USER_TOKEN')})
        self.assertEqual(res.status_code, 403)

    def test_get_user_by_id_404(self):
        res = self.client().get('/users/1000',
                                headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        self.assertEqual(res.status_code, 404)

    """
    delete_user_by_id should respond only to admin,
    401 if no token present
    403 if token doesn't have the permissions
    404 if the id doesn't exists
    """

    def test_delete_user_by_id(self):
        user = User(name="Test",
                    telephone="11111")
        user.insert()

        users_before_delete = User.total_users()

        res = self.client().delete('/users/' + str(user.id),
                                   headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})

        users_after_delete = User.total_users()

        self.assertTrue(users_before_delete - users_after_delete == 1)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['delete'])

    def test_delete_user_by_id_401(self):
        res = self.client().delete('/users/1')
        self.assertEqual(res.status_code, 401)

    def test_delete_user_by_id_403(self):
        res = self.client().delete('/users/1',
                                   headers={'Authorization': "Bearer " + os.getenv('USER_TOKEN')})
        self.assertEqual(res.status_code, 403)

    def test_delete_user_by_id_404(self):
        res = self.client().delete('/users/1000',
                                   headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        self.assertEqual(res.status_code, 404)

    """
    get_tag should respond to admin and user,
    401 if no token present
    404 if the id doesn't exists
    """

    def test_get_tag_by_admin(self):
        res = self.client().get('/tags/1',
                                headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['tag'])

    def test_get_tag_by_user(self):
        res = self.client().get('/tags/1',
                                headers={'Authorization': "Bearer " + os.getenv('USER_TOKEN')})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['tag'])

    def test_get_tag_401(self):
        res = self.client().get('/tags/1')
        self.assertEqual(res.status_code, 401)

    def test_get_tag_404(self):
        res = self.client().get('/tags/1000',
                                headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    """
    create_tag should respond to admin and user,
    401 if no token present
    """

    def test_create_tag_by_admin(self):
        tags_before_insert = Tag.total_tags()

        response = self.client().post('/tags',
                                      json=self.test_tag,
                                      headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        data = json.loads(response.data)

        tags_after_insert = Tag.total_tags()

        self.assertTrue(tags_after_insert - tags_before_insert == 1)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_create_tag_by_user(self):
        tags_before_insert = Tag.total_tags()

        response = self.client().post('/tags',
                                      json=self.test_tag,
                                      headers={'Authorization': "Bearer " + os.getenv('USER_TOKEN')})
        data = json.loads(response.data)

        tags_after_insert = Tag.total_tags()

        self.assertTrue(tags_after_insert - tags_before_insert == 1)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_create_tag_401(self):
        res = self.client().post('/tags')
        self.assertEqual(res.status_code, 401)


    """
    patch_tag should respond to admin and user,
    401 if no token present
    """

    def test_patch_tag_by_admin(self):
        response = self.client().patch('/tags/1',
                                       json=self.test_patch_tag,
                                       headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_tag_by_user(self):
        response = self.client().patch('/tags/1',
                                       json=self.test_patch_tag,
                                       headers={'Authorization': "Bearer " + os.getenv('USER_TOKEN')})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_tag_401(self):
        res = self.client().post('/tags')
        self.assertEqual(res.status_code, 401)

    """
    delete_tag should respond only to admin,
    401 if no token present
    403 if token doesn't have the permissions
    404 if the id doesn't exists
    """

    def test_delete_tag_by_admin(self):
        tag = Tag(name="Test",
                  information="11111",
                  user_id=1)
        tag.insert()

        tags_before_delete = Tag.total_tags()

        res = self.client().delete('/tags/' + str(tag.id),
                                   headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})

        tags_after_delete = Tag.total_tags()

        self.assertTrue(tags_before_delete - tags_after_delete == 1)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['delete'])

    def test_delete_tag_by_user(self):
        tag = Tag(name="Test",
                  information="11111",
                  user_id=1)
        tag.insert()

        tags_before_delete = Tag.total_tags()

        res = self.client().delete('/tags/' + str(tag.id),
                                   headers={'Authorization': "Bearer " + os.getenv('USER_TOKEN')})

        tags_after_delete = Tag.total_tags()

        self.assertTrue(tags_before_delete - tags_after_delete == 1)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['delete'])

    def test_delete_tag_401(self):
        res = self.client().delete('/tags/1')
        self.assertEqual(res.status_code, 401)

    def test_delete_tag_404(self):
        res = self.client().delete('/tags/1000',
                                   headers={'Authorization': "Bearer " + os.getenv('ADMIN_TOKEN')})
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
