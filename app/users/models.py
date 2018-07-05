from flask_restplus import fields
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


# user model fields and types
user_fields = dict(
    username=fields.String,
    first_name=fields.String,
    second_name=fields.String,
    email=fields.String,
    user_type=fields.String
)
