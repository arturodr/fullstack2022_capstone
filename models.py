import os
import uuid

from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy

import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
User
Has name and telephone
'''


class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    telephone = Column(String)

    def __init__(self, name, telephone=""):
        self.name = name
        self.telephone = telephone

    @staticmethod
    def total_users():
        return db.session.query(User).count()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'telephone': self.telephone}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback(self)


'''
Tag
Has name, a generated UUID, information and a related user
'''


class Tag(db.Model):
    __tablename__ = 'Tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tag_id = Column(String, unique=True)
    information = Column(String)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, name, information="", user_id=None):
        self.name = name
        self.tag_id = str(uuid.uuid4())[:8]
        self.information = information
        self.user_id = user_id

    @staticmethod
    def total_tags():
        return db.session.query(Tag).count()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'tag_id': self.tag_id,
            'information': self.information,
            'user_id': self.user_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback(self)