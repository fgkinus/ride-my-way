"""A simple users database implemented using a Dictionary"""
from passlib.hash import pbkdf2_sha256 as sha256


def generate_hash(password):
    """Hash all passwords """
    return sha256.hash(password)


def verify_hash(password, hash):
    """validate passwords against existing hashes"""
    return sha256.verify(password, hash)


def encrypt_passwords(data):
    """
    apply hashing to existing simple db
    :param data:
    :return data:
    """
    for user in data:
        user['password'] = generate_hash(user['password'])
    return data


user_data = [
    {
        "id": 1,
        "first_name": "john",
        "second_name": "smith",
        "username": "jsmith",
        "email": "jsmith@email.com",
        "password": "password",
        "user_type": "driver"
    },
    {
        "id": 2,
        "first_name": "jane",
        "second_name": "doe",
        "username": "jdoe",
        "email": "jdoe@email.com",
        "password": "password",
        "user_type": "driver"
    },
    {
        "id": 3,
        "first_name": "jack",
        "second_name": "ripper",
        "username": "jrip",
        "email": "jripper@email.com",
        "password": "password",
        "user_type": "passenger"
    },
    {
        "id": 4,
        "first_name": "norman",
        "second_name": "bates",
        "username": "psycho",
        "email": "psycho@email.com",
        "password": "password",
        "user_type": "passenger"
    }
]
users = encrypt_passwords(user_data)

# from v1 import db
# from datetime import datetime
# from flask_sqlalchemy import Model, SQLAlchemy
# import sqlalchemy as sa
# from sqlalchemy.ext.declarative import declared_attr, has_inherited_table
# from  v1.rides.models import Vehicles
#
# class BaseMixin(object):
#     """base template for models"""
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
#
#
# class User(BaseMixin, db.Model):
#     """
#     a basic user account
#     """
#     __tablename__ = 'User'
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     username = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(220), nullable=False)
#     profile = db.relationship('Profile', backref='user', lazy=True,
#                               uselist=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
#
# class Profile(db.Model):
#     """
#     A user profile class
#     """
#     __tablename__ = 'profile'
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     first_name = db.Column(db.String(120), nullable=False)
#     second_name = db.Column(db.String(120), nullable=False)
#     sur_name = db.Column(db.String(120), nullable=False)
#     account_type = db.Column(db.String(120), nullable=False)
#     vehicles = db.relationship('Vehicle')
#     ride_offers = db.relationship('RideOffers')
#
