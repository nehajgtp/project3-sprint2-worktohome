#tests app.py

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

