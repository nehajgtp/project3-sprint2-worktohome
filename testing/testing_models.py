#tests models.py
from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import models
import os


KEY_INPUT = "input"
KEY_EXPECTED = "expected"

POSITIVE_TESTING_PARAMETERS = [{KEY_INPUT : "!!!NOT DONE", KEY_EXPECTED: ""},\
{KEY_INPUT : "!!NOT DONE", KEY_EXPECTED: True},\
{KEY_INPUT : {}, KEY_EXPECTED : True },\
{KEY_INPUT : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30, {}], KEY_EXPECTED : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30, {}]},\
{KEY_INPUT : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30], KEY_EXPECTED : ["9 Corn Drive, CityState, ZZ", 100000, 300000, 30]}]

def database_being_updated():
    return None
    
def database_has_test():
    return None
    
def check_listings():
    reference_not_perm = models.LISTINGS
    if(reference_not_perm):#Access listing
        return True
    return False
    
def check_class__table_defintion(testing_parameter):
    expected = testing_parameter.get(KEY_EXPECTED)
    input_data = testing_parameter.get(KEY_INPUT)
    input_string = input_data[0];  input_dist = input_data[3]
    input_low = input_data[1];  input_high = input_data[2]; 

    reference_not_perm = models.table_defintion(input_string, input_low, input_high, input_dist, {})
    if(reference_not_perm.listings == expected[4] and reference_not_perm.address == expected[0]):#use is instead of == ?????
        #Consider checking search_data if possible
        return True
    return False
    
def check_class__search_parameters(testing_parameter):
    expected = testing_parameter.get(KEY_EXPECTED)
    input_data = testing_parameter.get(KEY_INPUT)
    input_string = input_data[0];  input_dist = input_data[3]
    input_low = input_data[1];  input_high = input_data[2]; 

    reference_not_perm = models.search_parameters(input_string, input_low, input_high, input_dist)
    if(reference_not_perm.distance == expected[3] and reference_not_perm.address == expected[0]):
        if(reference_not_perm.price_range_low == expected[1] and reference_not_perm.price_range_high == expected[2]):
            return True
    return False
    
if __name__ == '__main__':
    unittest.main()
    for()