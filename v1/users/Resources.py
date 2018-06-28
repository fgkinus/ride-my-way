import json

from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from flask_restplus import reqparse, Resource, fields, marshal_with

from v1 import connect_db
from v1.users import models
from db.utils import query_db

# database connection
DB = connect_db()
cursor = DB[1]

# data parsers
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)

reg_parser = reqparse.RequestParser()
reg_parser.add_argument('username', help='This field cannot be blank', required=True)
reg_parser.add_argument('first_name', help='This field cannot be blank', required=True)
reg_parser.add_argument('second_name', help='This field cannot be blank', required=True)
reg_parser.add_argument('email', help='This field cannot be blank', required=True)
reg_parser.add_argument('password', help='This field cannot be blank', required=True)
reg_parser.add_argument('user_type', help='This field cannot be blank', required=True)

edit_user_parser = reqparse.RequestParser()
edit_user_parser.add_argument('username', help='This field cannot be blank', required=True)
edit_user_parser.add_argument('first_name', help='This field  be blank', required=False)
edit_user_parser.add_argument('second_name', help='This field  be blank', required=False)
edit_user_parser.add_argument('email', help='This field  be blank', required=False)
edit_user_parser.add_argument('password', help='This field  cannot be blank', required=True)
edit_user_parser.add_argument('user_type', help='This field  be blank', required=False)

# output parsers
user_fields = dict(
    username=fields.String,
    first_name=fields.String,
    second_name=fields.String,
    email=fields.String,
    user_type=fields.String
)


class UserList(Resource):
    # @jwt_required
    @marshal_with(user_fields, envelope='users')
    def get(self):
        """
        :return a list of all users:
        """
        query = """SELECT * FROM user_accounts"""
        try:
            all_users = query_db(DB[0], query, None)
        except:
            return {
                'message ': " Error getting user list"
            }
        return all_users


class UserRegistration(Resource):
    def post(self):
        """
        Add new user
        :return :
        """
        data = reg_parser.parse_args()  # parse input
        query = """INSERT INTO user_accounts(username,first_name,second_name,email,password,user_type) 
                  VALUES (%s,%s,%s,%s,%s,%s)"""
        param = (data['username'], data['first_name'], data['second_name'],
                 data['email'], data['password'], data['user_type'],)

        try:
            query_db(DB[0], query=query, args=param)
        except:
            return {
                "error": "username or email address not unique"
            }
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return {'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': data
                }, 201

    @jwt_required
    def patch(self):
        data = edit_user_parser.parse_args()
        current_user = get_jwt_identity()
        query = """SELECT username,first_name,second_name,email,password,user_type FROM user_accounts 
                              WHERE username = %s AND password = %s"""
        param = (current_user, data['password'])
        # get current logged in user details
        try:
            user = query_db(DB[0], query, param)
            if len(user) != 1:
                raise Exception("invalid password")
        except Exception:
            return {
                       "message": "invalid Credentials",
                   }, 401
        # get all non null data entries
        for key in data.keys():
            if data[key] is None:
                data[key] = user[0][key]
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
RETURNING TRUE    
        """
        param = (data['username'], data['first_name'], data['second_name'],
                 data['email'], data['password'], data['user_type'], current_user)
        query_db(conn=DB[0], query=query, args=param)
        try:
            query_db(conn=DB[0], query=query, args=param)
            access_token = create_access_token(identity=data['username'])
            return {
                'message': 'user details updated',
                'access-token' : access_token,
                'details': data
            }
        except:
            return {
                       'message': 'Could not update your details'
                   }, 500


class UserLogin(Resource):
    def post(self):
        """
        start new user session
        :return dictionary:
        """
        data = login_parser.parse_args()
        try:
            query = """SELECT username,first_name,second_name,email FROM user_accounts 
                      WHERE username = %s AND password = %s"""
            param = (data['username'], data['password'])
            try:
                user = query_db(conn=DB[0], query=query, args=param)
            except Exception:
                raise Exception("error fetching")
            if len(user) == 1:
                access_token = create_access_token(identity=data['username'])
                refresh_token = create_refresh_token(identity=data['username'])
                return {
                    'message': 'Logged in as {}'.format(data['username']),
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user
                }
            else:
                return {
                           'message': 'invalid credentials'
                       }, 401
        except:
            return {
                       'message': 'Error processing request'
                   }, 400


class UserLogout(Resource):
    """The logout functionality right now is empty due to absence of
    a db to store revoked JWT tokens.
    """

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        query = """INSERT INTO jwt_blacklist(jwt) VALUES (%s)"""
        param = (jti)
        try:
            res = query_db(conn=DB[0], query=query, args=param)
            return {"msg": "Successfully logged out"}, 200
        except:
            return {"msg": "Unsuccessful log out"}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {
            'access_token': access_token
        }
