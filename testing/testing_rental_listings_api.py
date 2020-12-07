from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import os
import unittest.mock as mock
from mock import patch, call
import rental_listings_api
import requests

from rental_listings_api import HOME_CITY, HOME_STREET, HOME_POSTAL_CODE,\
                            HOME_STATE_CODE, HOME_STATE, HOME_COUNTY, \
                            HOME_PRICE, HOME_BATHS, HOME_BEDS, HOME_IMAGE, \
                            HOME_LAT, HOME_LON, IFRAME_URL, COMMUTE_TIME,\
                            HOME_WALKSCORE, WALKSCORE_DESCRIPTION, \
                            WALKSCORE_LOGO, WALKSCORE_MORE_INFO_LINK,\
                            HOME_WALKSCORE_LINK
KEY_INPUT = "input"
KEY_EXPECTED = "execpted"
CITY = "city"
STATE_CODE = "state_code"
MIN_PRICE = "min_price"
MAX_PRICE = "max_price"
ABSOLUTE_ADDRESS="absolute_address"
 
class MockedResponse:
    def __init__(self, json_data):
        self.json_data = json_data
    def json(self):
        return self.json_data
        
class MockGetRentalListings(unittest.TestCase):
    def setUp(self):
        self.success_test_params = {
            KEY_INPUT:{
            CITY: "Newark",
            STATE_CODE: "NJ",
            MIN_PRICE: 0,
            MAX_PRICE: 2000,
            ABSOLUTE_ADDRESS: "Newark, NJ"
            },
            KEY_EXPECTED:[{
                HOME_CITY: "Newark",
                HOME_STREET:"141 Summit Street",
                HOME_POSTAL_CODE:"07103",
                HOME_STATE_CODE:"34",
                HOME_STATE: "NJ",
                HOME_PRICE:2000,
                HOME_BATHS:2,
                HOME_BEDS:2,
                HOME_IMAGE:"filler_url",
                HOME_LON:"filler_longitude",
                HOME_LAT:"filler_latitude",
                IFRAME_URL:"some url",
                COMMUTE_TIME : "something",
                HOME_WALKSCORE:"hello",
                WALKSCORE_DESCRIPTION:"sup",
                WALKSCORE_LOGO:"something",
                WALKSCORE_MORE_INFO_LINK:"something",
                HOME_WALKSCORE_LINK:"something else"
            },
            {
                HOME_CITY: "Newark",
                HOME_STREET:"141 Summit Street",
                HOME_POSTAL_CODE:"07103",
                HOME_STATE_CODE:"34",
                HOME_STATE: "NJ",
                HOME_COUNTY: "Essex",
                HOME_PRICE:2000,
                HOME_BATHS:2,
                HOME_BEDS:2,
                IFRAME_URL: "some url",
                COMMUTE_TIME : "something",
                HOME_IMAGE:"filler_url",
                HOME_LON:"filler_longitude",
                HOME_LAT:"filler_latitude",
                HOME_WALKSCORE:"hello",
                WALKSCORE_DESCRIPTION:"sup",
                WALKSCORE_LOGO:"something",
                WALKSCORE_MORE_INFO_LINK:"something",
                HOME_WALKSCORE_LINK:"something else"
            }]
        }
    
    def mock_request(self, get, url, headers, params):
        d = {
            "meta":{
                "returned_rows":1
            },
            "properties":[
                {
                    "photo_count":1,
                    "photos":[
                        {
                            "href": "filler_url"
                        }
                    ],
                    "community":{
                        "price_min":2000,
                        "baths_min":2,
                        "beds_min":2,
                    },
                    "address":{
                        "line":"141 Summit Street",
                        "city":"Newark",
                        "state": "NJ",
                        "state_code":"34",
                        "lon":"filler_longitude",
                        "lat":"filler_latitude",
                        "postal_code":"07103"
                    }
                }
            ]
        }
        r = MockedResponse(d)
        return r
        
    def mock_get_walkscore_info(self,line, city, state_code, lon, lat):
        return {
            "walkscore" : "hello",
            "description": "sup",
            "logo" : "something",
            "more_info_link":"something",
            "walkscore_link":"something else"
        }
    def mock_generate_iframe_url(self, origin, destination):
        return "some url"
        
    def mock_get_place_id(self, address):
        return "some place"
        
    def mock_geocode(self, address):
        return "geocode"
    
    def mock_directions(self, address, address2, mode, departure_time):
        return [{
                "legs":[
                    {
                    "duration":{
                        "text" : "something"
                        }
                    }
                ]   
        }]
    def test_get_rental_listings(self):
        test_case = self.success_test_params
        with mock.patch("requests.request", self.mock_request):
            with mock.patch("walkscore_api.get_walkscore_info", self.mock_get_walkscore_info):
                with mock.patch("google_maps_api.get_place_id", self.mock_get_place_id):
                    with mock.patch("google_maps_api.generate_iframe_url", self.mock_generate_iframe_url):
                        with mock.patch("googlemaps.Client.directions", self.mock_directions):
                            inp = test_case[KEY_INPUT]
                            result = rental_listings_api.get_rental_listings(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE],inp[ABSOLUTE_ADDRESS])
                            # for result in results:
                            self.assertDictEqual(result[0], test_case[KEY_EXPECTED][0])
    
    def test_get_rental_listings_HTTPError(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as MockErr:
            MockErr.side_effect = requests.exceptions.HTTPError
            inp = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE],inp[ABSOLUTE_ADDRESS])
            
    def test_get_rental_listings_ConnectionError(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as MockErr:
            MockErr.side_effect = requests.exceptions.ConnectionError
            inp = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE],inp[ABSOLUTE_ADDRESS])
            
    def test_get_rental_listings_Timeout(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as MockErr:
            MockErr.side_effect = requests.exceptions.Timeout
            inp = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE],inp[ABSOLUTE_ADDRESS])
            
    def test_get_rental_listings_RequestException(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as MockErr:
            MockErr.side_effect = requests.exceptions.RequestException
            inp = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE],inp[ABSOLUTE_ADDRESS])
            
    def test_get_rental_listings_IndexError(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as MockErr:
            MockErr.side_effect = IndexError
            inp = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE],inp[ABSOLUTE_ADDRESS])
        
    def test_get_rental_listings_KeyError(self):
        test_case = self.success_test_params
        with mock.patch("requests.request") as MockErr:
            MockErr.side_effect = KeyError
            inp = test_case[KEY_INPUT]
            result = rental_listings_api.get_rental_listings(inp[CITY], inp[STATE_CODE], inp[MIN_PRICE], inp[MAX_PRICE],inp[ABSOLUTE_ADDRESS])
        
if __name__ == "__main__":
    unittest.main()