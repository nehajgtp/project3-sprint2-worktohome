'''
This file tests app.py
'''
import unittest

import os
import unittest.mock as mock
from mock import patch

from os.path import dirname, join
import sys

sys.path.append(join(dirname(__file__), "../"))
import app


KEY_INPUT = "input"
KEY_EXPECTED = "expected"

POSITIVE_TESTING_PARAMETERS = [
    {KEY_INPUT: "!!!NOT DONE", KEY_EXPECTED: ""},
    {KEY_INPUT: "!!NOT DONE", KEY_EXPECTED: True},
    {KEY_INPUT: {}, KEY_EXPECTED: True},
    {
        KEY_INPUT: ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30, {}],
        KEY_EXPECTED: ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30, {}],
    },
    {
        KEY_INPUT: ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30],
        KEY_EXPECTED: ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30],
    },
]
EMAIL = "email"
ADDRESS = "address"
PRICE_RANGE_LOW = "price_range_low"
PRICE_RANGE_HIGH = "price_range_high"
CITY = "city"
STATE = "state"
DISTANCE = "max_commute"
MIN_PRICE = "min_price"
MAX_PRICE = "max_price"
PURCHASE_TYPE = "purchase_type"


class MockParsingSearchParameters(unittest.TestCase):
    '''
    Class that mocks parameters
    '''
    def setUp(self):
        '''
        Makes test cases
        '''
        self.success_test_params = {
            KEY_INPUT: {
                ADDRESS: "141 Summit Street",
                CITY: "Newark",
                STATE: "NJ",
                DISTANCE: "40",
                MIN_PRICE: 100,
                MAX_PRICE: 2000,
                PURCHASE_TYPE: "sale",
            },
            KEY_EXPECTED: None,
        }
        self.success_test_params_rental = {
            KEY_INPUT: {
                ADDRESS: "141 Summit Street",
                CITY: "Newark",
                STATE: "NJ",
                DISTANCE: "40",
                MIN_PRICE: 100,
                MAX_PRICE: 2000,
                PURCHASE_TYPE: "rent",
            },
            KEY_EXPECTED: None,
        }
        self.success_test_invalid_min = {
            KEY_INPUT: {
                ADDRESS: "141 Summit Street",
                CITY: "Newark",
                STATE: "NJ",
                DISTANCE: "40",
                MIN_PRICE: -100,
                MAX_PRICE: 2000,
                PURCHASE_TYPE: "sale",
            },
            KEY_EXPECTED: None,
        }
        self.success_test_invalid_max = {
            KEY_INPUT: {
                ADDRESS: "141 Summit Street",
                CITY: "Newark",
                STATE: "NJ",
                DISTANCE: "40",
                MIN_PRICE: 100,
                MAX_PRICE: -2000,
                PURCHASE_TYPE: "sale",
            },
            KEY_EXPECTED: None,
        }

    def mock_get_homes(self, city, state, min_price, max_price, absolute_address):
        '''
        mocks get_homes
        '''
        return -1

    def mock_get_rental_listings(self, city, state, min_price, max_price, absolute_address):
        '''
        mocks get_rental_listings
        '''
        return -1

    def mock_get_homes_exists(self, city, state, min_price, max_price, absolute_address):
        '''
        mocks get_homes_exists
        '''
        return 1

    def mock_send_to_database(self, email, address, price_range_low,
                              price_range_high, city, state, purchase_type):
        '''
        mocks send_to_database
        '''
        return None

    @patch("flask_socketio.SocketIO.emit")
    def test_parse_search_parameters(self, mock_socket):
        '''
        Regular search
        '''
        test_case = self.success_test_params
        with mock.patch("app.send_to_database", self.mock_send_to_database):
            with mock.patch("apifunctions.get_homes", self.mock_get_homes):
                result = app.parsing_search_parameters(test_case[KEY_INPUT])
                mock_socket.assert_called_with("sending listing", [])

    @patch("flask_socketio.SocketIO.emit")
    def test_parse_search_parameters_rental(self, mock_socket):
        '''
        Rental Search
        '''
        test_case = self.success_test_params_rental
        with mock.patch("app.send_to_database", self.mock_send_to_database):
            with mock.patch(
                    "rental_listings_api.get_rental_listings", self.mock_get_rental_listings
            ):
                result = app.parsing_search_parameters(test_case[KEY_INPUT])
                mock_socket.assert_called_with("sending listing", [])

    @patch("flask_socketio.SocketIO.emit")
    def test_parse_search_parameters_exists(self, mock_socket):
        '''
        Parameters must exist
        '''
        test_case = self.success_test_params
        with mock.patch("app.send_to_database", self.mock_send_to_database):
            with mock.patch("apifunctions.get_homes", self.mock_get_homes_exists):
                result = app.parsing_search_parameters(test_case[KEY_INPUT])
                mock_socket.assert_called_with("sending listing", 1)

    def test_parse_search_min_error(self):
        '''
        handles underflow
        '''
        test_case = self.success_test_invalid_min
        with mock.patch("app.send_to_database", self.mock_send_to_database):
            with mock.patch("apifunctions.get_homes", self.mock_get_homes):
                result = app.parsing_search_parameters(test_case[KEY_INPUT])

    def test_parse_search_max_error(self):
        '''
        handles overflow
        '''
        test_case = self.success_test_invalid_max
        with mock.patch("app.send_to_database", self.mock_send_to_database):
            with mock.patch("apifunctions.get_homes", self.mock_get_homes):
                result = app.parsing_search_parameters(test_case[KEY_INPUT])


class MockDisplayTable(unittest.TestCase):
    '''
    Mocks table
    '''
    def setUp(self):
        '''
        ...
        '''
        self.success_test_params = {KEY_INPUT: "asdf@njit.edu", KEY_EXPECTED: None}

    def mock_db_query(self):
        '''
        Regular query
        '''
        return ["hello", "hello"]

    def mock_db_query_no_rows(self):
        '''
        No results
        '''
        return None

    @patch("flask_socketio.SocketIO.emit")
    def test_displayTable(self, mock_socket):
        '''
        Pretends to send a table
        '''
        test_case = self.success_test_params
        with mock.patch("app.DB.session") as mock_query:
            mock_query.query.return_value.filter_return_value.all.return_value = (
                self.mock_db_query()
            )
            result = app.display_table()
            self.assertTrue(mock_socket.called)
            mock_socket.assert_called_with("received database info", [])

    @patch("flask_socketio.SocketIO.emit")
    def test_displayTable_norows(self, mock_socket):
        '''
        Pretends to send a empty table
        '''
        test_case = self.success_test_params
        with mock.patch("app.DB.session", new_callable=mock.PropertyMock) as mock_query:
            mock_query.query.return_value.filter_return_value.all.return_value = (
                self.mock_db_query_no_rows()
            )
            result = app.display_table()
            # self.assertTrue(mock_socket.called)
            mock_socket.assert_called_with("received database info", [])


if __name__ == "__main__":
    unittest.main()
