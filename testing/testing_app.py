#tests app.py
from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))


import unittest
import app
import os
import unittest.mock as mock
from mock import patch

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

POSITIVE_TESTING_PARAMETERS = [{KEY_INPUT : "!!!NOT DONE", KEY_EXPECTED: ""},\
{KEY_INPUT : "!!NOT DONE", KEY_EXPECTED: True},\
{KEY_INPUT : {}, KEY_EXPECTED : True },\
{KEY_INPUT : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30, {}], KEY_EXPECTED : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30, {}]},\
{KEY_INPUT : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30], KEY_EXPECTED : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30]}]
EMAIL = "email"
ADDRESS = "address"
PRICE_RANGE_LOW = "price_range_low"
PRICE_RANGE_HIGH = "price_range_high"
CITY = "city"
STATE = "state"
DISTANCE = "max_commute"
MIN_PRICE = "min_price"
MAX_PRICE = "max_price"
# class MockSendToDatabase(unittest.TestCase):
#     def setUp(self):
#         self.success_test_params = {
#             KEY_INPUT: {
#                 EMAIL: "kevinng250",
#                 ADDRESS: "141 Summit Street, Newark, NJ",
#                 PRICE_RANGE_LOW: "100",
#                 PRICE_RANGE_HIGH: "2000" 
#             },
#             KEY_EXPECTED: ""
#         }
class MockParsingSearchParameters(unittest.TestCase):
    def setUp(self):
        self.success_test_params = {
            KEY_INPUT: {
                ADDRESS:"141 Summit Street",
                CITY:"Newark",
                STATE:"NJ",
                DISTANCE:"40",
                MIN_PRICE:"100",
                MAX_PRICE:"2000"
            },
            KEY_EXPECTED: None
        }
        
    def mock_get_homes(self, city, state, min_price, max_price):
        return -1
    def mock_send_To_database(self, email, address, price_range_low, price_range_high, distance):
        return None
    def test_parse_search_parameters(self):
        test_case = self.success_test_params
        with mock.patch("app.sendToDatabase", self.mock_send_To_database):
            with mock.patch("apifunctions.getHomes", self.mock_get_homes):
                result = app.parsing_search_parameters(test_case[KEY_INPUT])
                self.assertEqual(result, test_case[KEY_EXPECTED])