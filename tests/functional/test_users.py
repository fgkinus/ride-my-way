from flask_jwt_extended import create_access_token, create_refresh_token

from tests.functional.test_rides import json_of_response


class TestUserEndpoints(object):
    def test_get_users(self, test_client):
        """test that all users are displayed"""
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = test_client.get('api/v2/auth/users', headers=headers)
        assert response.status_code == 200
        json_data = json_of_response(response)
        assert isinstance(json_data, dict)
        assert 'users' in json_data
        assert isinstance(json_data['users'], list)

    def test_login(self, test_client):
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = test_client.post('api/v2/auth/login', headers=headers,
                                    data={
                                        'username': 'testuser',
                                        'password': 'password'
                                    })
        assert response.status_code == 200

    def test_logout(self, test_client):
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = test_client.delete('api/v2/auth/logout', headers=headers)
        json_data = json_of_response(response)
        assert response.status_code == 200
        assert 'msg' in json_data

    def test_refresh_with_access_token(self, test_client):
        access_token = create_access_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = test_client.post('api/v2/auth/refresh', headers=headers)
        json_data = json_of_response(response)
        assert response.status_code == 401
        assert 'message' in json_data

    def test_refresh_with_refresh_token(self, test_client):
        access_token = create_refresh_token('testuser')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = test_client.post('api/v2/auth/refresh', headers=headers)
        json_data = json_of_response(response)
        assert response.status_code == 200
        assert 'access_token' in json_data

    def test_user_registration(self, test_client):
        """add a user"""
        response = test_client.post(
            'api/v2/auth/register',
            data={
                "username": "testuser1",
                "first_name": "thika",
                "second_name": "Lavington",
                "email": "value@email.com",
                "password": "probox",
                "user_type": "passenger",
            }
        )
        assert response.status_code == 200 or response.status_code == 201
        json_data = json_of_response(response)
        assert "error" in json_data or "access_token" in json_data
