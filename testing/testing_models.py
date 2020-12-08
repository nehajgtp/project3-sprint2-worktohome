'''
tests models.py
'''
from os.path import dirname, join
import sys
import unittest
import models
sys.path.append(join(dirname(__file__), "../"))



KEY_INPUT = "input"
KEY_EXPECTED = "expected"

POSITIVE_TESTING_PARAMETERS = [
    {
        KEY_INPUT: {
            "email": "hello@njit.edu",
            "address": "9 Corn Drive, CityState, ZZ",
            "price_range_low": 100000,
            "price_range_high": 300000,
            "distance": 10,
        },
        KEY_EXPECTED: True,
    },
    {
        KEY_INPUT: [
            "hello@njit.edu",
            "9 Corn Drive, CityState, ZZ",
            100000,
            300000,
            "CityState",
            "ZZ",
            "sale",
        ],
        KEY_EXPECTED: [
            "hello@njit.edu",
            "9 Corn Drive, CityState, ZZ",
            100000,
            300000,
            "CityState",
            "ZZ",
            "sale",
        ],
    },
    {
        KEY_INPUT: ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30],
        KEY_EXPECTED: ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30],
    },
]


class TestingModels(unittest.TestCase):
    '''
    Main Class
    '''
    def setUp(self):
        '''
        Sets up variables
        '''
        self.success_test_params = [
            {
                KEY_INPUT: [
                    "hello@njit.edu",
                    "9 Corn Drive, CityState, ZZ",
                    100000,
                    300000,
                    "CityState",
                    "ZZ",
                    "sale",
                ],
                KEY_EXPECTED: [
                    "hello@njit.edu",
                    "9 Corn Drive, CityState, ZZ",
                    100000,
                    300000,
                    "CityState",
                    "ZZ",
                    "sale",
                ],
            }
        ]

    def check_class__table_defintion(self, testing_parameter):
        '''
        Main function
        '''
        expected = testing_parameter[KEY_EXPECTED]
        input_data = testing_parameter[KEY_INPUT]
        input_address = input_data[1]
        input_email = input_data[0]
        input_low = input_data[2]
        input_high = input_data[3]
        input_city = input_data[4]
        input_state = input_data[5]
        input_purchase_type = input_data[6]
        reference_not_perm = models.TableDefintion(
            input_email,
            input_address,
            input_low,
            input_high,
            input_city,
            input_state,
            input_purchase_type,
        )
        if (
                reference_not_perm.email == expected[0]
                and reference_not_perm.address == expected[1]
        ):  # use is instead of == ?????
            if (
                    reference_not_perm.price_low == expected[2]
                    and reference_not_perm.price_high == expected[3]
            ):
                if (
                        reference_not_perm.city == expected[4]
                        and reference_not_perm.state == expected[5]
                        and reference_not_perm.purchase_type == expected[6]
                ):
                    return True
        return False

    def test_success_test_params(self):
        '''
        Defining the tests
        '''
        test_eval = self.check_class__table_defintion(POSITIVE_TESTING_PARAMETERS[1])

if __name__ == "__main__":
    unittest.main()
