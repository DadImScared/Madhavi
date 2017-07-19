
import os

import config
from peewee import *

from flask_bcrypt import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

dir_path = os.path.dirname(os.path.realpath(__file__))

DATABASE = SqliteDatabase('{}{}people.db'.format(dir_path, os.path.sep))


class BaseModel(Model):
    class Meta:
        database = DATABASE


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()

    @classmethod
    def create_user(cls, username, password, **kwargs):
        """Return User object"""
        try:
            return cls.create(
                username=username,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("User already exists")

    @classmethod
    def get_user(cls, username):
        try:
            return cls.get(cls.username==username)
        except DoesNotExist:
            return None

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        else:
            user = User.get(User.id==data['id'])
            return user

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def update_password(self, password):
        self.password = generate_password_hash(password)
        self.save()
        return self

    def generate_auth_token(self, expires=3600):
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})


class Post(Model):
    user = ForeignKeyField(User, related_name='to_user')
    content = TextField()
    page_name = CharField(unique=True)
    page_display = CharField(unique=True)
    page_order = IntegerField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_post(cls, user, content, page_name, page_display, page_order):
        try:
            return cls.create(user=user, content=content, page_name=page_name,
                       page_display=page_display, page_order=page_order)
        except IntegrityError:
            return None

    @classmethod
    def get_post(cls, page_name, user=None):
        try:
            return cls.get(cls.page_name==page_name)
        except DoesNotExist:
            pass


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()
