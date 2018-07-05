from flask_jwt_extended import create_access_token

from tests.functional.test_rides import json_of_response


class TestUserEndpoints(object):
    def test_get_users(self, test_client):
        """test that all users are displayed"""
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = test_client.get('api/v1/auth/users', headers=headers)
        assert response.status_code == 200
        json_data = json_of_response(response)
        assert isinstance(json_data, dict)
        assert 'users' in json_data
        assert isinstance(json_data['users'], list)

    def test_user_registration(self):
        """add a user"""
