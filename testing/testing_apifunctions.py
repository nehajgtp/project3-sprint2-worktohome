'''
This file tests apifunctions.py
'''
from os.path import dirname, join
import sys
import unittest
import os
import unittest.mock as mock
import requests
import io
from mock import patch, call
sys.path.append(join(dirname(__file__), "../"))

import apifunctions

from apifunctions import (
    HOME_CITY,
    HOME_STREET,
    HOME_POSTAL_CODE,
    HOME_STATE_CODE,
    HOME_STATE,
    HOME_COUNTY,
    HOME_PRICE,
    HOME_BATHS,
    HOME_BEDS,
    HOME_IMAGE,
    HOME_LAT,
    HOME_LON,
    IFRAME_URL,
    COMMUTE_TIME,
    HOME_WALKSCORE,
    WALKSCORE_DESCRIPTION,
    WALKSCORE_LOGO,
    WALKSCORE_MORE_INFO_LINK,
    HOME_WALKSCORE_LINK,
)

import google_maps_api

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

PROPERTY_ID = "property_id"
MIN_PRICE = "min_price"
MAX_PRICE = "max_price"
ABSOLUTE_ADDRESS = "absolute_address"

CITY = "city"
STATE_CODE = "state_code"


class MockedResponse:
    '''
    Class that mocks the response
    '''
    def __init__(self, json_data):
        '''
        ...
        '''
        self.json_data = json_data

    def json(self):
        '''
        ...
        '''
        return self.json_data


class MockNearbyHomes(unittest.TestCase):
    '''
    Main Class
    '''
    def setUp(self):
        '''
        Creates testing parameters
        '''
        self.success_test_params = {
            KEY_INPUT: {
                PROPERTY_ID: "111111",
                MIN_PRICE: 0,
                MAX_PRICE: 1000000,
                ABSOLUTE_ADDRESS: "141 Summit St, Newark, NJ",
            },
            KEY_EXPECTED: [
                {
                    HOME_CITY: "Newark",
                    HOME_STREET: "141 Summit Street",
                    HOME_POSTAL_CODE: "07103",
                    HOME_STATE_CODE: 34,
                    HOME_STATE: "NJ",
                    HOME_COUNTY: "Essex",
                    HOME_PRICE: 2000,
                    HOME_BATHS: 2,
                    HOME_BEDS: 2,
                    HOME_IMAGE: "filler_url",
                    HOME_LON: "filler_longitude",
                    HOME_LAT: "filler_latitude",
                    IFRAME_URL: "some url",
                    COMMUTE_TIME: "something",
                    HOME_WALKSCORE: "hello",
                    WALKSCORE_DESCRIPTION: "sup",
                    WALKSCORE_LOGO: "something",
                    WALKSCORE_MORE_INFO_LINK: "something",
                    HOME_WALKSCORE_LINK: "something else",
                }
            ],
        }

    def mock_success_requests(self, method, url, headers, params):
        variables = {
            "data": {
                "home": {
                    "related_homes": {
                        "results": [
                            {
                                "list_price": 2000,
                                "location": {
                                    "address": {
                                        "line": "141 Summit Street",
                                        "city": "Newark",
                                    }
                                },
                                "description": {"baths": 2, "beds": 2},
                                "primary_photo": {"href": "filler_url"},
                            }
                        ]
                    }
                }
            }
        }
        response = MockedResponse(variables)
        return response

    def mock_success_geocode(self, address):
        '''
        Mocks sucessful geocode
        '''
        return [
            {
                "address_components": [
                    "",
                    "",
                    "",
                    {"long_name": "Essex"},
                    {"short_name": 34, "long_name": "NJ"},
                    "",
                    {"long_name": "07103"},
                ],
                "geometry": {
                    "location": {"lng": "filler_longitude", "lat": "filler_latitude"}
                },
            }
        ]

    def mock_walkscore_info(self, home_street, home_city, home_state_code, home_lon, home_lat):
        '''
        Mocks walkscore_info
        '''
        return {
            "walkscore": "hello",
            "description": "sup",
            "logo": "something",
            "more_info_link": "something",
            "walkscore_link": "something else",
        }

    def mock_generate_iframe_url(self, origin, destination):
        '''
        Mocks generate_iframe_url
        '''
        return "some url"

    def mock_get_place_id(self, address):
        '''
        mocks get_place_id
        '''
        return "some place"

    def mock_directions(self, address, address2, mode, departure_time):
        '''
        mocks the directions
        '''
        return [{"legs": [{"duration": {"text": "something"}}]}]

    def test_nearbyhomes_success(self):
        '''
        mocks nearbyhomes
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request", self.mock_success_requests):
            with mock.patch("googlemaps.Client.geocode", self.mock_success_geocode):
                with mock.patch("google_maps_api.get_place_id", self.mock_get_place_id):
                    with mock.patch(
                        "google_maps_api.generate_iframe_url",
                        self.mock_generate_iframe_url,
                    ):
                        with mock.patch(
                            "googlemaps.Client.directions", self.mock_directions
                        ):
                            with mock.patch(
                                "walkscore_api.get_walkscore_info",
                                self.mock_walkscore_info,
                            ):
                                input_case = test_case[KEY_INPUT]
                                results = apifunctions.nearby_homes(
                                    input_case[PROPERTY_ID],
                                    input_case[MIN_PRICE],
                                    input_case[MAX_PRICE],
                                    input_case[ABSOLUTE_ADDRESS],
                                )
                                for result in results:
                                    # print(result)
                                    # print(test_case[KEY_EXPECTED][0])
                                    self.assertDictEqual(
                                        result, test_case[KEY_EXPECTED][0]
                                    )

    # def mock_stdout(self):
    #     return "getHomes API : Http Error: ", requests.exceptions.HTTPError

    def mock_http_error_requests(self, method, url, headers, params):
        '''
        Bad HTTP error handling
        '''
        return requests.exceptions.HTTPError

    def test_nearbyhomes_http_err(self):
        '''
        Checks error handling for HTTP
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = requests.exceptions.HTTPError
            input_case = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(
                input_case[PROPERTY_ID], input_case[MIN_PRICE], input_case[MAX_PRICE], input_case[ABSOLUTE_ADDRESS]
            )

    def test_nearbyhomes_connection_err(self):
        '''
        Checks some kind of Connection Error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = requests.exceptions.ConnectionError
            input_case = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(
                input_case[PROPERTY_ID], input_case[MIN_PRICE], input_case[MAX_PRICE], input_case[ABSOLUTE_ADDRESS]
            )

    def test_nearbyhomes_timeout(self):
        '''
        Checks timeout error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = requests.exceptions.Timeout
            input_case = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(
                input_case[PROPERTY_ID], input_case[MIN_PRICE], input_case[MAX_PRICE], input_case[ABSOLUTE_ADDRESS]
            )

    def test_nearbyhomes_request_exception(self):
        '''
        Checks a genenic bad request handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = requests.exceptions.RequestException
            input_case = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(
                input_case[PROPERTY_ID], input_case[MIN_PRICE], input_case[MAX_PRICE], input_case[ABSOLUTE_ADDRESS]
            )

    def test_nearbyhomes_index_err(self):
        '''
        Check index error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = IndexError
            input_case = test_case[KEY_INPUT]
            result = apifunctions.nearby_homes(
                input_case[PROPERTY_ID], input_case[MIN_PRICE], input_case[MAX_PRICE], input_case[ABSOLUTE_ADDRESS]
            )


class MockGetHomes(unittest.TestCase):
    '''
    Mocks the other function
    '''
    def setUp(self):
        '''
        Sets up testing parameters
        '''
        self.success_test_params = {
            KEY_INPUT: {
                CITY: "Newark",
                STATE_CODE: "34",
                MIN_PRICE: 0,
                MAX_PRICE: 1000000,
                ABSOLUTE_ADDRESS: "141 Summit St, Newark, NJ",
            },
            KEY_EXPECTED: [
                {
                    HOME_CITY: "Newark",
                    HOME_STREET: "141 Summit Street",
                    HOME_POSTAL_CODE: "07103",
                    HOME_STATE_CODE: "34",
                    HOME_STATE: "NJ",
                    HOME_PRICE: 2000,
                    HOME_BATHS: 2,
                    HOME_BEDS: 2,
                    HOME_IMAGE: "filler_url",
                    HOME_LON: "filler_longitude",
                    HOME_LAT: "filler_latitude",
                    IFRAME_URL: "some url",
                    COMMUTE_TIME: "something",
                    HOME_WALKSCORE: "hello",
                    WALKSCORE_DESCRIPTION: "sup",
                    WALKSCORE_LOGO: "something",
                    WALKSCORE_MORE_INFO_LINK: "something",
                    HOME_WALKSCORE_LINK: "something else",
                },
                {
                    HOME_CITY: "Newark",
                    HOME_STREET: "141 Summit Street",
                    HOME_POSTAL_CODE: "07103",
                    HOME_STATE_CODE: "34",
                    HOME_STATE: "NJ",
                    HOME_COUNTY: "Essex",
                    HOME_PRICE: 2000,
                    HOME_BATHS: 2,
                    HOME_BEDS: 2,
                    HOME_IMAGE: "filler_url",
                    HOME_LON: "filler_longitude",
                    HOME_LAT: "filler_latitude",
                    IFRAME_URL: "some url",
                    COMMUTE_TIME: "something",
                    HOME_WALKSCORE: "hello",
                    WALKSCORE_DESCRIPTION: "sup",
                    WALKSCORE_LOGO: "something",
                    WALKSCORE_MORE_INFO_LINK: "something",
                    HOME_WALKSCORE_LINK: "something else",
                },
            ],
        }
        self.success_test_params_no_properties = {
            KEY_INPUT: {
                CITY: "Newark",
                STATE_CODE: "34",
                MIN_PRICE: 0,
                MAX_PRICE: 1000000,
                ABSOLUTE_ADDRESS: "141 Summit Street, Newark, NJ",
            },
            KEY_EXPECTED: -1,
        }
        self.success_test_params_no_thumbnail = {
            KEY_INPUT: {
                CITY: "Newark",
                STATE_CODE: 34,
                MIN_PRICE: 0,
                MAX_PRICE: 1000000,
                ABSOLUTE_ADDRESS: "141 Summit Street, Newark, NJ",
            },
            KEY_EXPECTED: [
                {
                    HOME_CITY: "Newark",
                    HOME_STREET: "141 Summit Street",
                    HOME_POSTAL_CODE: "07103",
                    HOME_STATE_CODE: "34",
                    HOME_STATE: "NJ",
                    HOME_PRICE: 2000,
                    HOME_BATHS: 2,
                    HOME_BEDS: 2,
                    HOME_IMAGE: "DEFAULT_IMAGE",
                    HOME_LON: "filler_longitude",
                    HOME_LAT: "filler_latitude",
                    IFRAME_URL: "some url",
                    COMMUTE_TIME: "something",
                    HOME_WALKSCORE: "hello",
                    WALKSCORE_DESCRIPTION: "sup",
                    WALKSCORE_LOGO: "something",
                    WALKSCORE_MORE_INFO_LINK: "something",
                    HOME_WALKSCORE_LINK: "something else",
                },
                {
                    HOME_CITY: "Newark",
                    HOME_STREET: "141 Summit Street",
                    HOME_POSTAL_CODE: "07103",
                    HOME_STATE_CODE: "34",
                    HOME_STATE: "NJ",
                    HOME_COUNTY: "Essex",
                    HOME_PRICE: 2000,
                    HOME_BATHS: 2,
                    HOME_BEDS: 2,
                    HOME_IMAGE: "filler_url",
                    HOME_LON: "filler_longitude",
                    HOME_LAT: "filler_latitude",
                    IFRAME_URL: "some url",
                    COMMUTE_TIME: "something",
                    HOME_WALKSCORE: "hello",
                    WALKSCORE_DESCRIPTION: "sup",
                    WALKSCORE_LOGO: "something",
                    WALKSCORE_MORE_INFO_LINK: "something",
                    HOME_WALKSCORE_LINK: "something else",
                },
            ],
        }

    def mock_success_requests_properties(self, method, url, headers, params):
        '''
        sucessful requests
        '''
        variables = {
            "meta": {"returned_rows": 2},
            "properties": [
                {
                    "thumbnail": "filler_url",
                    "price": 2000,
                    "address": {
                        "city": "Newark",
                        "line": "141 Summit Street",
                        "postal_code": "07103",
                        "state_code": "34",
                        "state": "NJ",
                        "lon": "filler_longitude",
                        "lat": "filler_latitude",
                    },
                    "baths": 2,
                    "beds": 2,
                    "property_id": 12345,
                },
                {
                    "thumbnail": "filler_url",
                    "price": 10000000,
                    "address": {
                        "city": "Newark",
                        "line": "141 Summit Street",
                        "postal_code": "07103",
                        "state_code": 34,
                        "state": "NJ",
                        "lon": "filler_longitude",
                        "lat": "filler_latitude",
                    },
                    "baths": 2,
                    "beds": 2,
                    "property_id": 12345,
                },
            ],
        }
        response = MockedResponse(variables)
        return response

    def mock_nearby_homes(self, PROPERTY_ID, MIN_PRICE, MAX_PRICE, ABSOLUTE_ADDRESS):
        '''
        Mocks nearby_homes
        '''
        return [
            {
                HOME_CITY: "Newark",
                HOME_STREET: "141 Summit Street",
                HOME_POSTAL_CODE: "07103",
                HOME_STATE_CODE: "34",
                HOME_STATE: "NJ",
                HOME_COUNTY: "Essex",
                HOME_PRICE: 2000,
                HOME_BATHS: 2,
                HOME_BEDS: 2,
                HOME_IMAGE: "filler_url",
                HOME_LON: "filler_longitude",
                HOME_LAT: "filler_latitude",
                IFRAME_URL: "some url",
                COMMUTE_TIME: "something",
                HOME_WALKSCORE: "hello",
                WALKSCORE_DESCRIPTION: "sup",
                WALKSCORE_LOGO: "something",
                WALKSCORE_MORE_INFO_LINK: "something",
                HOME_WALKSCORE_LINK: "something else",
            }
        ]

    def mock_walkscore_info(self, home_street, home_city, home_state_code, home_lon, home_lat):
        '''
        Mocks walkscore_info
        '''
        return {
            "walkscore": "hello",
            "description": "sup",
            "logo": "something",
            "more_info_link": "something",
            "walkscore_link": "something else",
        }

    def mock_generate_iframe_url(self, origin, destination):
        '''
        Mocks generate_iframe_url
        '''
        return "some url"

    def mock_get_place_id(self, address):
        '''
        get_place_id
        '''
        return "some place"

    def mock_geocode(self, address):
        '''
        mocks geocode
        '''
        return "geocode"

    def mock_directions(self, address, address2, mode, departure_time):
        '''
        mocks directions
        '''
        return [{"legs": [{"duration": {"text": "something"}}]}]

    def test_gethomes_success(self):
        '''
        does the testing
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request", self.mock_success_requests_properties):
            with mock.patch("apifunctions.nearby_homes", self.mock_nearby_homes):
                with mock.patch(
                    "walkscore_api.get_walkscore_info", self.mock_walkscore_info
                ):
                    with mock.patch(
                        "google_maps_api.generate_iframe_url",
                        self.mock_generate_iframe_url,
                    ):
                        with mock.patch(
                            "google_maps_api.get_place_id", self.mock_get_place_id
                        ):
                            with mock.patch(
                                "googlemaps.Client.directions", self.mock_directions
                            ):
                                inp = test_case[KEY_INPUT]
                                results = apifunctions.get_homes(
                                    inp[CITY],
                                    inp[STATE_CODE],
                                    inp[MIN_PRICE],
                                    inp[MAX_PRICE],
                                    inp[ABSOLUTE_ADDRESS],
                                )
                                print(inp[MIN_PRICE])
                                print(inp[MAX_PRICE])
                                for i in range(len(results)):
                                    self.assertDictEqual(
                                        results[i], test_case[KEY_EXPECTED][i]
                                    )

    def mock_success_requests_properties_none(self, method, url, headers, params):
        '''
        on sucess 
        '''
        variables = {"meta": {"returned_rows": 0}}
        response = MockedResponse(variables)
        return response

    def test_getHomes_success_no_properties(self):
        '''
        sucessful but no properties
        '''
        test_case = self.success_test_params_no_properties
        with mock.patch("requests.request", self.mock_success_requests_properties_none):
            with mock.patch("apifunctions.nearby_homes", self.mock_nearby_homes):
                with mock.patch(
                    "walkscore_api.get_walkscore_info", self.mock_walkscore_info
                ):
                    with mock.patch(
                        "google_maps_api.generate_iframe_url",
                        self.mock_generate_iframe_url,
                    ):
                        with mock.patch(
                            "google_maps_api.get_place_id", self.mock_get_place_id
                        ):
                            with mock.patch(
                                "googlemaps.Client.directions", self.mock_directions
                            ):
                                inp = test_case[KEY_INPUT]
                                results = apifunctions.get_homes(
                                    inp[CITY],
                                    inp[STATE_CODE],
                                    inp[MIN_PRICE],
                                    inp[MAX_PRICE],
                                    inp[ABSOLUTE_ADDRESS],
                                )
                                self.assertEquals(results, test_case[KEY_EXPECTED])

    def mock_success_requests_properties_no_thumbnail(
        self, method, url, headers, params
    ):
        '''
        mocks the properties of the requests
        '''
        variables = {
            "meta": {"returned_rows": 1},
            "properties": [
                {
                    "price": 2000,
                    "address": {
                        "city": "Newark",
                        "line": "141 Summit Street",
                        "postal_code": "07103",
                        "state_code": "34",
                        "state": "NJ",
                        "lon": "filler_longitude",
                        "lat": "filler_latitude",
                    },
                    "baths": 2,
                    "beds": 2,
                    "property_id": 12345,
                }
            ],
        }
        response = MockedResponse(variables)
        return response

    def test_gethomes_success_no_thumbnail(self):
        '''
        Homes that have no picture
        '''
        test_case = self.success_test_params_no_thumbnail
        with mock.patch(
            "requests.request", self.mock_success_requests_properties_no_thumbnail
        ):
            with mock.patch("apifunctions.nearby_homes", self.mock_nearby_homes):
                with mock.patch(
                    "walkscore_api.get_walkscore_info", self.mock_walkscore_info
                ):
                    with mock.patch(
                        "google_maps_api.generate_iframe_url",
                        self.mock_generate_iframe_url,
                    ):
                        with mock.patch(
                            "google_maps_api.get_place_id", self.mock_get_place_id
                        ):
                            with mock.patch(
                                "googlemaps.Client.directions", self.mock_directions
                            ):
                                inp = test_case[KEY_INPUT]
                                results = apifunctions.get_homes(
                                    inp[CITY],
                                    inp[STATE_CODE],
                                    inp[MIN_PRICE],
                                    inp[MAX_PRICE],
                                    inp[ABSOLUTE_ADDRESS],
                                )
                                for i in range(len(results)):
                                    self.assertDictEqual(
                                        results[i], test_case[KEY_EXPECTED][i]
                                    )

    # @patch('requests.request')
    # @patch('apifunctions.nearbyHomes')
    # @patch('builtins.print')
    def test_gethomes_http_err(self):
        '''
        Checks error handling for HTTP
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = requests.exceptions.HTTPError
            input_case = test_case[KEY_INPUT]
            result = apifunctions.get_homes(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_gethomes_connection_err(self):
        '''
        Checks some kind of Connection Error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = requests.exceptions.ConnectionError
            input_case = test_case[KEY_INPUT]
            result = apifunctions.get_homes(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_gethomes_timeout(self):
        '''
        Checks timeout error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = requests.exceptions.Timeout
            input_case = test_case[KEY_INPUT]
            result = apifunctions.get_homes(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_gethomes_request_exception(self):
        '''
        Checks a genenic bad request handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = requests.exceptions.RequestException
            input_case = test_case[KEY_INPUT]
            result = apifunctions.get_homes(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_gethomes_index_err(self):
        '''
        Check index error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as bar_mock:
            bar_mock.side_effect = IndexError
            input_case = test_case[KEY_INPUT]
            result = apifunctions.get_homes(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )


class MockGetPlaceId(unittest.TestCase):
    '''
    Class designated to mock place_id
    '''
    def setUp(self):
        '''
        ....
        '''
        self.success_test_params = {
            KEY_INPUT: "141 Summit St, Newark, NJ",
            KEY_EXPECTED: "some_id",
        }

    def mock_find_place(self, address, input_type):
        '''
        mocks find_place
        '''
        return {"candidates": [{"place_id": "some_id"}]}

    def test_get_place_id(self):
        '''
        Checks place_id
        '''
        test_case = self.success_test_params
        with mock.patch("googlemaps.Client.find_place", self.mock_find_place):
            result = google_maps_api.get_place_id(test_case[KEY_INPUT])
            self.assertEqual(result, test_case[KEY_EXPECTED])


if __name__ == "__main__":
    unittest.main()
