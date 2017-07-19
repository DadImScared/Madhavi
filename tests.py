
import unittest
from flask_testing import TestCase
from server.app import create_app
from server.settings import TestingConfig
import inspect
import sys
from abc import ABCMeta
from playhouse.test_utils import test_database
from base64 import b64encode

import config
from models import *

new_database = SqliteDatabase(':memory:')


class TestCaseWithPeewee(TestCase):

    __metaclass__ = ABCMeta

    def run(self, result=None):
        model_classes = [m[1] for m in inspect.getmembers(sys.modules['models'], inspect.isclass) if
                         issubclass(m[1], Model) and m[1] != Model]
        with test_database(new_database, model_classes):
            super(TestCaseWithPeewee, self).run(result)


class BaseTestCase(TestCaseWithPeewee):

    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        self.name = config.ADMIN_NAME
        self.password = config.ADMIN_PASS
        user = User.create_user(self.name, self.password)
        Post.create_post(user, "content here", "home", "Home", 0)

    def test_create_user(self):
        User.create_user("user1", "password")
        self.assertEqual(2, User.select().count())

    def test_user_login_token_refresh(self):
        info = {
            'username': self.name,
            'password': self.password
        }
        response = self.client.post('/api/v1/users', data=info)
        self.assert200(response)
        token = response.json['token']
        headers = {
            "Authorization": 'Basic {}'.format(b64encode((token + ':').encode('utf-8')).decode('utf-8'))
        }
        response = self.client.get('/api/v1/users/token', headers=headers)
        self.assert200(response)

    def test_update_user(self):
        info = {
            'username': self.name,
            'password': self.password
        }
        response = self.client.post('/api/v1/users', data=info)
        self.assert200(response)
        token = response.json['token']

        # test for miss matched new_password and confirm_new_password
        data = {
            "current_password": self.password,
            "new_password": "password1",
            "confirm_new_password": "awdawdga"
        }
        headers = {
            "Authorization": 'Basic {}'.format(b64encode((token + ':').encode('utf-8')).decode('utf-8'))
        }
        response2 = self.client.patch('/api/v1/users', headers=headers, data=data)
        self.assert401(response2)
        self.assertEqual("passwords must match", response2.json["message"])

        # test for successful password change
        data["confirm_new_password"] = "password1"
        response3 = self.client.patch('/api/v1/users', headers=headers, data=data)
        self.assert200(response3)
        self.assertEqual("Info updated!", response3.json["message"])

        # test login failed with old password after password change
        response = self.client.post('/api/v1/users', data=info)
        self.assert401(response)

        # test successful login with new password after password change
        info['password'] = 'password1'
        response = self.client.post('/api/v1/users', data=info)
        self.assert200(response)

    def test_post_page(self):
        headers = {
            "Authorization": 'Basic {}'.format(b64encode((self.name + ':' + self.password).encode('utf-8')).decode('utf-8'))
        }
        old_post_count = Post.select().count()
        new_post = {"content": "content 2 here", "page_name": "about", "page_display": "About", "page_order": 1}
        response = self.client.post('/api/v1/posts', data=new_post, headers=headers)
        new_post_count = Post.select().count()
        self.assertNotEquals(old_post_count, new_post_count)
        self.assertEquals(new_post["content"], response.json["content"])
        self.assert200(response)

    def test_patch_page(self):
        self.assertEqual('content here', Post.select().get().content)
        headers = {
            "Authorization": 'Basic {}'.format(b64encode((self.name + ':' + self.password).encode('utf-8')).decode('utf-8'))
        }
        info = {'content': 'test content here'}
        response = self.client.patch('/api/v1/posts/home', data=info, headers=headers)
        self.assertEqual('test content here', Post.select().get().content)
        self.assert200(response)

    def test_mail_services(self):
        data = {
            "name": "Fake Name",
            "email": "FakeName@FakeDomain.com",
            "message": "this is a fake message"
        }
        response = self.client.post('/api/v1/services/mail', data=data)
        self.assert200(response)

if __name__ == '__main__':
    unittest.main()
