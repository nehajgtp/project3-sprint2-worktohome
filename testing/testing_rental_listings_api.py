'''
This file tests rental_listings_api
'''
from os.path import dirname, join
import sys
import unittest
import os
import unittest.mock as mock
from mock import patch, call
import rental_listings_api
import requests

sys.path.append(join(dirname(__file__), "../"))


from rental_listings_api import (
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

KEY_INPUT = "input"
KEY_EXPECTED = "execpted"
CITY = "city"
STATE_CODE = "state_code"
MIN_PRICE = "min_price"
MAX_PRICE = "max_price"
ABSOLUTE_ADDRESS = "absolute_address"


class MockedResponse:
    '''
    Class that mocks responses
    '''
    def __init__(self, json_data):
        '''
        Create class
        '''
        self.json_data = json_data

    def json(self):
        '''
        ...
        '''
        return self.json_data


class MockGetRentalListings(unittest.TestCase):
    '''
    Main Class
    '''
    def setUp(self):
        '''
        Creates the test parameters
        '''
        self.success_test_params = {
            KEY_INPUT: {
                CITY: "Newark",
                STATE_CODE: "NJ",
                MIN_PRICE: 0,
                MAX_PRICE: 2000,
                ABSOLUTE_ADDRESS: "Newark, NJ",
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
                    IFRAME_URL: "some url",
                    COMMUTE_TIME: "something",
                    HOME_IMAGE: "filler_url",
                    HOME_LON: "filler_longitude",
                    HOME_LAT: "filler_latitude",
                    HOME_WALKSCORE: "hello",
                    WALKSCORE_DESCRIPTION: "sup",
                    WALKSCORE_LOGO: "something",
                    WALKSCORE_MORE_INFO_LINK: "something",
                    HOME_WALKSCORE_LINK: "something else",
                },
            ],
        }

    def mock_request(self, get, url, headers, params):
        '''
        Creates the request
        '''
        variables = {
            "meta": {"returned_rows": 1},
            "properties": [
                {
                    "photo_count": 1,
                    "photos": [{"href": "filler_url"}],
                    "community": {
                        "price_min": 2000,
                        "baths_min": 2,
                        "beds_min": 2,
                    },
                    "address": {
                        "line": "141 Summit Street",
                        "city": "Newark",
                        "state": "NJ",
                        "state_code": "34",
                        "lon": "filler_longitude",
                        "lat": "filler_latitude",
                        "postal_code": "07103",
                    },
                }
            ],
        }
        response = MockedResponse(variables)
        return response

    def mock_get_walkscore_info(self, line, city, state_code, lon, lat):
        '''
        mocks function get_walkscore_info
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

    def test_get_rental_listings(self):
        '''
        Gets the test variables
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request", self.mock_request):
            with mock.patch(
                    "walkscore_api.get_walkscore_info", self.mock_get_walkscore_info
            ):
                with mock.patch("google_maps_api.get_place_id", self.mock_get_place_id):
                    with mock.patch(
                            "google_maps_api.generate_iframe_url",
                            self.mock_generate_iframe_url,
                    ):
                        with mock.patch(
                                "googlemaps.Client.directions", self.mock_directions
                        ):
                            input_case = test_case[KEY_INPUT]
                            result = rental_listings_api.get_rental_listings(
                                input_case[CITY],
                                input_case[STATE_CODE],
                                input_case[MIN_PRICE],
                                input_case[MAX_PRICE],
                                input_case[ABSOLUTE_ADDRESS],
                            )
                            # for result in results:
                            self.assertDictEqual(result[0], test_case[KEY_EXPECTED][0])

    def test_get_rental_listings_http_err(self):
        '''
        Checks error handling for HTTP
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as mock_err:
            mock_err.side_effect = requests.exceptions.HTTPError
            input_case = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_get_rental_listings_connection_err(self):
        '''
        Checks some kind of Connection Error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as mock_err:
            mock_err.side_effect = requests.exceptions.ConnectionError
            input_case = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_get_rental_listings_timeout(self):
        '''
        Checks timeout error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as mock_err:
            mock_err.side_effect = requests.exceptions.Timeout
            input_case = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_get_rental_listings_request_exception(self):
        '''
        Checks a genenic bad request handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as mock_err:
            mock_err.side_effect = requests.exceptions.RequestException
            input_case = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_get_rental_listings_index_err(self):
        '''
        Check index error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as mock_err:
            mock_err.side_effect = IndexError
            input_case = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )

    def test_get_rental_listings_key_error(self):
        '''
        Checks key error handling
        '''
        test_case = self.success_test_params
        with mock.patch("requests.request") as mock_err:
            mock_err.side_effect = KeyError
            input_case = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(
                input_case[CITY],
                input_case[STATE_CODE],
                input_case[MIN_PRICE],
                input_case[MAX_PRICE],
                input_case[ABSOLUTE_ADDRESS],
            )


if __name__ == "__main__":
    unittest.main()
