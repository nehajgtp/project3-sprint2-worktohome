'''
This file tests walkscore_api
'''
from os.path import dirname, join
import sys
import unittest
import os
import unittest.mock as mock
from mock import patch, call

import requests
sys.path.append(join(dirname(__file__), "../"))
import walkscore_api


KEY_INPUT = "key_input"
KEY_EXPECTED = "key_expected"


class MockedResponse:
    '''
    Defines functions that get data
    '''
    def __init__(self, json_data):
        '''
        creates the class
        '''
        self.json_data = json_data

    def json(self):
        '''
        ...
        '''
        return self.json_data


class MockGetWalkscoreInfo(unittest.TestCase):
    '''
    Main Class
    '''
    def setUp(self):
        self.success_test_params = {
            KEY_INPUT: {
                "home_street": "",
                "home_city": "",
                "home_state_code": "",
                "home_lon": "",
                "home_lat": "",
            },
            KEY_EXPECTED: {
                "walkscore": "hello",
                "description": "sup",
                "logo": "something",
                "more_info_link": "something",
                "walkscore_link": "something else",
            },
        }

    def mock_request(self, url):
        '''
        Mocks the request
        '''
        variables = {
            "walkscore": "hello",
            "description": "sup",
            "logo_url": "something",
            "more_info_link": "something",
            "ws_link": "something else",
        }
        response = MockedResponse(variables)
        return response

    def test_get_walkscore_info(self):
        '''
        Does the tests
        '''
        test_case = self.success_test_params
        with mock.patch("requests.get", self.mock_request):
            input_case = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(
                input_case["home_street"],
                input_case["home_city"],
                input_case["home_state_code"],
                input_case["home_lon"],
                input_case["home_lat"],
            )
            self.assertEqual(result, test_case[KEY_EXPECTED])

    def test_get_walkscore_info_http_err(self):
        '''
        Checks error handling for HTTP
        '''
        test_case = self.success_test_params
        with mock.patch("requests.get") as err_mock:
            err_mock.side_effect = requests.exceptions.HTTPError
            input_case = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(
                input_case["home_street"],
                input_case["home_city"],
                input_case["home_state_code"],
                input_case["home_lon"],
                input_case["home_lat"],
            )

    def test_get_walkscore_info_connection_err(self):
        '''
        Checks some kind of Connection Error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.get") as err_mock:
            err_mock.side_effect = requests.exceptions.ConnectionError
            input_case = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(
                input_case["home_street"],
                input_case["home_city"],
                input_case["home_state_code"],
                input_case["home_lon"],
                input_case["home_lat"],
            )

    def test_get_walkscore_info_timeout_err(self):
        '''
        Checks timeout error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.get") as err_mock:
            err_mock.side_effect = requests.exceptions.Timeout
            input_case = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(
                input_case["home_street"],
                input_case["home_city"],
                input_case["home_state_code"],
                input_case["home_lon"],
                input_case["home_lat"],
            )

    def test_get_walkscore_info_hrequest_exception(self):
        '''
        Checks a specific bad request handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.get") as err_mock:
            err_mock.side_effect = requests.exceptions.RequestException
            input_case = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(
                input_case["home_street"],
                input_case["home_city"],
                input_case["home_state_code"],
                input_case["home_lon"],
                input_case["home_lat"],
            )

    def test_get_walkscore_info_index_err(self):
        '''
        Check index error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.get") as err_mock:
            err_mock.side_effect = IndexError
            input_case = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(
                input_case["home_street"],
                input_case["home_city"],
                input_case["home_state_code"],
                input_case["home_lon"],
                input_case["home_lat"],
            )

if __name__ == "__main__":
    unittest.main()
