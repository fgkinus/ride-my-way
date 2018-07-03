import json

import pytest
from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager

from v1 import register_blueprints, init_db


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


@pytest.fixture
def test_client():
    app = Flask(__name__)
    init_db(db_name='testing')
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
    assert type(json_data['ride-offers']) == list

#
# def test_add_ride_offer(test_client):
#     """
#     verify by adding ride details
#     :param test_client:
#     :return:
#     """
#     access_token = create_access_token('testuser')
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
#     response = test_client.post(
#         '/api/v1/rides', headers=headers,
#         data={
#             "driver": "testuser",
#             "origin": "thika",
#             "destination": "Lavington",
#             "departure_time": "value",
#             "vehicle_model": "probox",
#             "vehicle_capacity": "4",
#             "route": "thika highway",
#         }
#     )
#     # verify a user who is not a river cannot add a request
#     json_data = json_of_response(response)
#     assert response.status_code == 401
#
#     # verify  a driver can add a ride offer
#     access_token = create_access_token('testdriver')
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
#     response = test_client.post(
#         '/api/v1/rides', headers=headers,
#         data={
#             "driver": "testdtiver",
#             "origin": "thika",
#             "destination": "Lavington",
#             "departure_time": "value",
#             "vehicle_model": "probox",
#             "vehicle_capacity": "4",
#             "route": "thika highway",
#         }
#     )
#     json_data = json_of_response(response)
#     assert response.status_code == 201
#     assert 'message' in json_data
#     assert 'trip' in json_data
#     assert json_data['trip']['driver'] == 'testdriver'
#     assert 'id' in json_data['trip']
#
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
#     assert 'ride-offers' in json_data
#     assert json_data['ride-offers'][0]['id'] == 1
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
#     assert 'ride-details' in json_data
#     assert isinstance(json_data['requests'], list) == isinstance(json_data['ride-details'], list)
#     assert json_data['ride-details'][0]['id'] == 1
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
#     assert 'request' in json_data
#     assert json_data['request'][0]['requester'] == 17
#     assert 'created' in json_data['request'][0]
#
#
# def test_get_ride_request_responses(test_client):
#     """
#     Test the return responses for a request endpoints
#     :param test_client:
#     :return:
#     """
#     access_token = create_access_token('testuser')
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
#     response = test_client.get('/api/v1/rides/1/responses', headers=headers)
#     json_data = json_of_response(response)
#     assert response.status_code == 200
#     assert 'response' in json_data
#     assert isinstance(json_data['response'], list)
#     assert json_data['response'][0]['request_id'] == 1
#
#     # ensure only integers can be passed as arguments
#     response = test_client.get('/api/v1/rides/str/responses', headers=headers)
#     assert response.status_code == 404
#     with pytest.raises(JSONDecodeError) as json_error:
#         json_data = json_of_response(response)
#
#     assert "Expecting value" in str(json_error)
