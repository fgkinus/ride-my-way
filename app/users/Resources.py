from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, WrongTokenError
from flask_restplus import reqparse, Resource, marshal_with, Namespace
from jwt import ExpiredSignature

from app.users.models import user_fields, User

# define a namespace for rides
api = Namespace('Auth', description='user accounts related operations')


# error handlers
@api.errorhandler(NoAuthorizationError)
def handle_no_auth_exception(error):
    """Handle ethe jwt required exception when none s provided"""
    return {'message': 'No authentication token provided'}, 401


@api.errorhandler(ExpiredSignature)
def handle_expired_token(error):
    return {'message': 'authentication token provided is expired'}, 401


@api.errorhandler(WrongTokenError)
def handle_expired_token(error):
    return {'message': 'Provide a refresh token rather than an access token'}, 401


# APi endpoints
@api.route('/users', endpoint="list-all-users")
class UserList(Resource):
    @jwt_required
    @marshal_with(user_fields, envelope='users')
    def get(self):
        """
        :return a list of all users:
        """
        user = User()
        try:
            all_users = user.get_users()
        except:
            return {
                'message ': " Error getting user list"
            }
        return all_users


@api.route('/register', endpoint="register-users")
class UserRegistration(Resource):
    """user registration view set """
    # init parsers
    reg_parser = reqparse.RequestParser()
    reg_parser.add_argument('username', help='This field cannot be blank', required=True)
    reg_parser.add_argument('first_name', help='This field cannot be blank', required=True)
    reg_parser.add_argument('second_name', help='This field cannot be blank', required=True)
    reg_parser.add_argument('email', help='This field cannot be blank', required=True)
    reg_parser.add_argument('password', help='This field cannot be blank', required=True)
    reg_parser.add_argument('user_type', help='This field cannot be blank', required=True)

    @api.expect(reg_parser)
    def post(self):
        """
        Add new user
        :return :
        """
        data = self.reg_parser.parse_args()  # parse input
        # user object
        user = User(data=data)
        # query accounts
        try:
            new_user = user.add_user()
        except:
            return {
                       "error": "username or email address not unique"
                   }, 200
        # create query tokens
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        # message and output
        return {'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': new_user
                }, 201


@api.route('/profile', endpoint="edit-users")
class UserProfileEdit(Resource):
    edit_user_parser = reqparse.RequestParser()
    edit_user_parser.add_argument('username', help='This field cannot be blank', required=True)
    edit_user_parser.add_argument('first_name', help='This field  be blank', required=False)
    edit_user_parser.add_argument('second_name', help='This field  be blank', required=False)
    edit_user_parser.add_argument('email', help='This field  be blank', required=False)
    edit_user_parser.add_argument('password', help='This field  cannot be blank', required=True)
    edit_user_parser.add_argument('new_password', help='This field  cannot be blank', required=False)
    edit_user_parser.add_argument('user_type', help='This field  be blank', required=False)

    @jwt_required
    @api.expect(edit_user_parser)
    def patch(self):
        """update user details for logged in user"""
        data = self.edit_user_parser.parse_args()
        current_user = get_jwt_identity()
        user = User(data=data)
        # get current logged in user details
        try:
            new_user = user.edit_user(current_user=current_user)
            if new_user is False:
                return {
                           'message': "Invalid password"
                       }, 401
        except Exception:
            return {
                       "message": "Error executing request",
                   }, 500

        try:
            access_token = create_access_token(identity=data['username'])
            return {
                'message': 'user details updated',
                'access-token': access_token,
                'details': new_user
            }
        except:
            return {
                       'message': 'Could not update your details'
                   }, 500


@api.route('/login', endpoint="login-users")
class UserLogin(Resource):
    """USer login viewset  """

    login_parser = reqparse.RequestParser()
    login_parser.add_argument('username', help='This field cannot be blank', required=True)
    login_parser.add_argument('password', help='This field cannot be blank', required=True)

    def post(self):
        """
        start new user session
        :return dictionary:
        """
        data = self.login_parser.parse_args()
        user = User(data=data)

        try:
            user = user.login()
        except Exception:
            return {
                       'message': "server error logging in"
                   }, 500
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


@api.route('/logout', endpoint="logout-users")
class UserLogout(Resource):
    """The logout functionality right now is empty due to absence of
    a db to store revoked JWT tokens.
    """

    @jwt_required
    def delete(self):
        """logout a user"""
        jti = get_raw_jwt()['jti']
        user = User()
        param = (jti,)
        try:
            user.logout(param)
            return {"msg": "Successfully logged out"}, 200
        except:
            return {"msg": "Unsuccessful log out"}, 500


@api.route('/refresh', endpoint="refresh-token")
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """refresh the access token for user"""
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {
            'access_token': access_token
        }
