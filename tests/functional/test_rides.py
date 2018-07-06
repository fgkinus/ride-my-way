import json
from json import JSONDecodeError

import pytest
from flask_jwt_extended import create_access_token, JWTManager


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


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
    response = test_client.get('/api/v2/rides', headers=headers)
    json_data = json_of_response(response)
    assert response.status_code == 200
    # if database is not empty
    if len(json_data) > 1:
        assert 'ride-offers' in json_data[0]
        assert isinstance(json_data[0]['ride-offers'], list)


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
        '/api/v2/rides', headers=headers,
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
    assert response.status_code == 401

    # verify  a driver can add a ride offer
    access_token = create_access_token('testdriver')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.post(
        '/api/v2/rides', headers=headers,
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



def test_get_specific_ride_offer(test_client):
    """
    test api endpoint ro return specific ride offer
    :param test_client:
    :return:
    """
    access_token = create_access_token('testuser')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.get('/api/v2/rides/1', headers=headers)
    json_data = json_of_response(response)
    assert response.status_code == 200
    assert 'ride-offers' in json_data
    assert json_data['ride-offers'][0]['id'] == 1


def test_get_ride_request_for_specific_ride_offer(test_client):
    """
    test api endpoint ro return specific ride offer and a list of offers
    :param test_client:
    :return:
    """
    access_token = create_access_token('testuser')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.get('/api/v2/rides/1/requests', headers=headers)
    json_data = json_of_response(response)
    assert response.status_code == 200
    assert 'requests' in json_data
    assert 'ride-details' in json_data
    assert isinstance(json_data['requests'], list) == isinstance(json_data['ride-details'], list)
    assert json_data['ride-details'][0]['id'] == 1


def test_add_ride_request_for_specific_ride_offer(test_client):
    """
    test api endpoint to add ride request for currently authenticated user
    :param test_client:
    :return:
    """
    access_token = create_access_token('testuser')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.post('/api/v2/rides/1/requests', headers=headers)
    json_data = json_of_response(response)
    assert response.status_code == 201
    assert 'message' in json_data
    assert 'request' in json_data
    assert json_data['request'][0]['requester'] == 17
    assert 'created' in json_data['request'][0]


def test_get_ride_request_responses(test_client):
    """
    Test the return responses for a request endpoints
    :param test_client:
    :return:
    """
    access_token = create_access_token('testuser')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = test_client.get('/api/v2/rides/1/response', headers=headers)
    json_data = json_of_response(response)
    if len(json_data) > 0:
        assert response.status_code == 200
        assert 'response' in json_data or 'message' in json_data
    else:
        assert response.status_code == 204

    # ensure only integers can be passed as arguments
    response = test_client.get('/api/v2/rides/str/response', headers=headers)
    assert response.status_code == 400
    json_data = json_of_response(response)
    assert 'error' in json_data
