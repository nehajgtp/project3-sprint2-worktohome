from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import os
import unittest.mock as mock
from mock import patch, call
import walkscore_api
import requests

KEY_INPUT = "key_input"
KEY_EXPECTED = "key_expected"
class MockedResponse:
    def __init__(self, json_data):
        self.json_data = json_data
    def json(self):
        return self.json_data

class MockGetWalkscoreInfo(unittest.TestCase):
    def setUp(self):
        self.success_test_params ={
            KEY_INPUT:{
                "home_street":"",
                "home_city":"",
                "home_state_code":"",
                "home_lon":"",
                "home_lat":""
                },
            KEY_EXPECTED:{
                "walkscore":"hello",
                "description":"sup",
                "logo":"something",
                "more_info_link":"something",
                "walkscore_link":"something else"
                }
        }
    def mock_request(self, url):
        d ={
            "walkscore":"hello",
            "description":"sup",
            "logo_url":"something",
            "more_info_link":"something",
            "ws_link":"something else"
        }
        r = MockedResponse(d)
        return r
        
    def test_get_walkscore_info(self):
        test_case = self.success_test_params
        with mock.patch("requests.get", self.mock_request):
            inp = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(inp["home_street"], inp["home_city"], \
                    inp["home_state_code"], inp["home_lon"], inp["home_lat"])
            self.assertEqual(result, test_case[KEY_EXPECTED])
            
    def test_get_walkscore_info_HTTPErr(self):
        test_case = self.success_test_params
        with mock.patch("requests.get") as errMock:
            errMock.side_effect = requests.exceptions.HTTPError
            inp = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(inp["home_street"], inp["home_city"], \
                    inp["home_state_code"], inp["home_lon"], inp["home_lat"])
                    
    def test_get_walkscore_info_ConnectionErr(self):
        test_case = self.success_test_params
        with mock.patch("requests.get") as errMock:
            errMock.side_effect = requests.exceptions.ConnectionError
            inp = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(inp["home_street"], inp["home_city"], \
                    inp["home_state_code"], inp["home_lon"], inp["home_lat"])
                    
    def test_get_walkscore_info_TimeoutErr(self):
        test_case = self.success_test_params
        with mock.patch("requests.get") as errMock:
            errMock.side_effect = requests.exceptions.Timeout
            inp = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(inp["home_street"], inp["home_city"], \
                    inp["home_state_code"], inp["home_lon"], inp["home_lat"])
                    
    def test_get_walkscore_info_HRequestException(self):
        test_case = self.success_test_params
        with mock.patch("requests.get") as errMock:
            errMock.side_effect = requests.exceptions.RequestException
            inp = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(inp["home_street"], inp["home_city"], \
                    inp["home_state_code"], inp["home_lon"], inp["home_lat"])
                    
    def test_get_walkscore_info_IndexError(self):
        test_case = self.success_test_params
        with mock.patch("requests.get") as errMock:
            errMock.side_effect = IndexError
            inp = test_case[KEY_INPUT]
            result = walkscore_api.get_walkscore_info(inp["home_street"], inp["home_city"], \
                    inp["home_state_code"], inp["home_lon"], inp["home_lat"])
    
if __name__ == "__main__":
    unittest.main()
