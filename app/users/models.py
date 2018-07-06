import psycopg2
from flask_restplus import fields
from passlib.hash import pbkdf2_sha256 as sha256

from app.utils import Database

# user model fields and types
user_fields = dict(
    username=fields.String,
    first_name=fields.String,
    second_name=fields.String,
    email=fields.String,
    user_type=fields.String
)


class User(object):
    """a class representing a user instance"""

    def __init__(self, data=None, database=Database):
        """initialise the user object with a DB instance and parsed data"""
        self.DB = database
        self.details = data

    @staticmethod
    def generate_hash(password):
        """Hash all passwords """
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        """validate passwords against existing hashes"""
        return sha256.verify(password, hash)

    def verify_data_is_dict(self):
        if not isinstance(self.details, dict):
            raise Exception("invalid data.Provide a  parsed dictionary")
        else:
            return True

    def add_user(self):
        """
        :param data:
        :return user:
        """
        data = self.details
        if self.verify_data_is_dict():
            query = """INSERT INTO user_accounts(username,first_name,second_name,email,password,user_type) 
                                      VALUES (%s,%s,%s,%s,%s,%s) returning *;"""
            param = (data['username'], data['first_name'], data['second_name'],
                     data['email'], data['password'], data['user_type'],)
            try:
                new_user = self.DB.query_db(query=query, args=param)
                return new_user
            except:
                raise psycopg2.DatabaseError("could not add new user")

    def get_users(self):
        """list all users"""
        query = """SELECT * FROM user_accounts"""
        all_users = self.DB.query_db(query, None)
        return all_users

    def get_user(self, username):
        """list all users"""
        query = """SELECT * FROM user_accounts where username = %s"""
        user = self.DB.query_db(query, (username,))
        return user

    def login(self):
        """validate users"""
        query = """SELECT username,first_name,second_name,email FROM user_accounts 
                              WHERE username = %s AND password = %s"""
        param = (self.details['username'], self.details['password'])
        user = self.DB.query_db(query=query, args=param)
        return user

    def logout(self, token):
        """blacklist token """
        query = """INSERT INTO jwt_blacklist(jwt) VALUES (%s)"""
        self.DB.query_db_no_result(query=query, args=(token,))

    def edit_user(self, current_user):
        """modify user details"""
        query = """SELECT username,first_name,second_name,email,password,user_type FROM user_accounts 
                                       WHERE username = %s AND password = %s"""
        user = self.login(username=current_user, password=self.details['password'])
        if len(user) != 1:
            return False
        else:
            # add dummy key
            user[0]['new_password'] = None
            """Fill blanks in data provided"""
            for key in self.details.keys():
                if self.details[key] is None:
                    self.details[key] = user[0][key]
            "check that there is a new password"
            if self.details['new_password'] is not None:
                self.details['password'] = self.details['new_password']
                # now run query to patch
            query = """
                                 UPDATE user_accounts
                                     SET username  = %s,
                                       first_name  = %s,
                                       second_name = %s,
                                       email       = %s,
                                       password    = %s,
                                       user_type   = %s
                                     WHERE username = %s     
                                     RETURNING *;    
                                 """
            data = self.details
            param = (data['username'], data['first_name'], data['second_name'],
                     data['email'], data['password'], data['user_type'], current_user)
            new_user = self.DB.query_db(query=query, args=param)
            return new_user
