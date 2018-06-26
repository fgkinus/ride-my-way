import json

from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity
from flask_restplus import reqparse, Resource, fields, marshal_with

from v1 import connect_db
from v1.users import models
from v1.users.models import verify_hash

# database connection
DB = connect_db('rmw', 'postgres', '')
cursor = DB[1]

# data parsers
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)

reg_parser = reqparse.RequestParser()
reg_parser.add_argument('username', help='This field cannot be blank', required=True)
reg_parser.add_argument('password', help='This field cannot be blank', required=True)
reg_parser.add_argument('email', help='This field cannot be blank', required=True)
reg_parser.add_argument('first_name', help='This field cannot be blank', required=True)
reg_parser.add_argument('second_name', help='This field cannot be blank', required=True)
reg_parser.add_argument('user_type', help='This field cannot be blank', required=True)

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
        cursor.execute(query)
        all_users = (cursor.fetchall())
        return all_users


class UserRegistration(Resource):
    def post(self):
        """
        Add new user
        :return dictionary:
        """
        data = reg_parser.parse_args()  # parse input
        models.users.append(data)  # add new user to list
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return {'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 201


class UserLogin(Resource):
    def post(self):
        """
        start new user session
        :return dictionary:
        """
        data = login_parser.parse_args()
        try:
            query = """SELECT username,first_name,second_name,email FROM user_accounts WHERE username = %s"""
            cursor.execute(query, (data['username'],))
            user = cursor.fetchall()
            if len(user) == 1:
                access_token = create_access_token(identity=data['username'])
                refresh_token = create_refresh_token(identity=data['username'])
                return jsonify({
                    'message': 'Logged in as {}'.format(data['username']),
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user
                })
        except:
            return jsonify({
                'message': 'Error processing request'
            }), 400


class UserLogout(Resource):
    """The logout functionality right now is empty due to absence of
    a db to store revoked JWT tokens.
    """

    @jwt_required
    def post(self):
        return jsonify({'message': 'good bye {}'.format(get_jwt_identity())})


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {
            'access_token': access_token
        }
