import json
import os
import tempfile
import pytest
from flask_jwt_extended import create_access_token, JWTManager

from v1 import create_app, register_blueprints, connect_db


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


@pytest.fixture
def test_client():
    app = create_app('testing')
    register_blueprints(app=app)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    # configure JWT
    app.config[
        'JWT_SECRET_KEY'] = '$pbkdf2-sha256$29000$I.T8f8/ZG8M4J0QIwTgHIA$.9wCvRZECxd7/yvHttEgoHzpvgjdhjizq5ySewKfeQc'
    jwt = JWTManager(app)
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()


def test_get_all_ride_requests(test_client):
    """
    check that rides are added via api
    :param test_client:
    :return:
    """
    access_token = create_access_token('testuser')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.get('/api/v1/rides', headers=headers)
    json_data = json_of_response(response)
    assert response.status_code == 200
    assert 'ride-offers' in json_data
    assert type(json_data['ride-offers']) ==list


def test_add_ride_offer(test_client):
    """
    verify by adding ride details
    :param test_client:
    :return:
    """
    access_token = create_access_token('testuser')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.post(
        '/api/v1/rides', headers=headers,
        data={
            "driver": "testuser",
            "origin": "thika",
            "destination": "Lavington",
            "departure_time": "value",
            "vehicle_model": "probox",
            "vehicle_capacity": "4",
            "route": "thika highway",
        }
    )
    # verify a user who is not a river cannot add a request
    json_data = json_of_response(response)
    assert response.status_code == 401

    # verify  a driver can add a ride offer
    access_token = create_access_token('testdriver')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.post(
        '/api/v1/rides', headers=headers,
        data={
            "driver": "testdtiver",
            "origin": "thika",
            "destination": "Lavington",
            "departure_time": "value",
            "vehicle_model": "probox",
            "vehicle_capacity": "4",
            "route": "thika highway",
        }
    )
    json_data = json_of_response(response)
    assert response.status_code == 201
    assert 'message' in json_data
    assert 'trip' in json_data
    assert json_data['trip']['driver'] == 'testdriver'
    assert 'id' in json_data['trip']

#
# def test_get_specific_ride_offer(test_client):
#     """
#     test api endpoint ro return specific ride offer
#     :param test_client:
#     :return:
#     """
#     access_token = create_access_token('testuser')
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
#     response = test_client.get('/api/v1/rides/1', headers=headers)
#     json_data = json_of_response(response)
#     assert response.status_code == 200
#     assert 'ride-offer' in json_data
#     assert json_data['ride-offer']['id'] == 1
#
#
# def test_get_ride_request_for_specific_ride_offer(test_client):
#     """
#     test api endpoint ro return specific ride offer and a list of offers
#     :param test_client:
#     :return:
#     """
#     access_token = create_access_token('testuser')
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
#     response = test_client.get('/api/v1/rides/1/requests', headers=headers)
#     json_data = json_of_response(response)
#     assert response.status_code == 200
#     assert 'requests' in json_data
#     assert 'ride' in json_data
#     assert json_data['ride'][0]['id'] == 1
#     assert len(json_data['requests']) == 2
#
#
# def test_add_ride_request_for_specific_ride_offer(test_client):
#     """
#     test api endpoint to add ride request for currently authenticated user
#     :param test_client:
#     :return:
#     """
#     access_token = create_access_token('testuser')
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
#     response = test_client.post('/api/v1/rides/1/requests', headers=headers)
#     json_data = json_of_response(response)
#     assert response.status_code == 201
#     assert 'message' in json_data
#     assert 'details' in json_data
#     assert json_data['details']['requester'] == 'testuser'
#     assert 'time' in json_data['details']
