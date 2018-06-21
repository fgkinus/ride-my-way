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
