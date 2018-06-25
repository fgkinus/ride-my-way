from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity
from flask_restplus import reqparse, Resource

from v1.users import models
from v1.users.models import verify_hash

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


class UserList(Resource):
    @jwt_required
    def get(self):
        """
        :return a list of all users:
        """
        return jsonify(models.users)


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
            user = [usr for usr in models.users if usr['username'] == data['username']
                    and verify_hash(data['password'], usr['password'])]
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
