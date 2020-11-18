import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import urllib

DOTENV_PATH = join(dirname(__file__), "apikeys.env")
load_dotenv(DOTENV_PATH)

WALKSCORE_API_KEY = os.getenv("WALKSCORE_API_KEY")

def get_walkscore_info(home_street, home_city, home_state_code, home_lon, home_lat):
    address = home_street + " " + home_city + " " + home_state_code
    encoded_address = urllib.parse.quote_plus(address)

    url = "https://api.walkscore.com/score?format=json&address=" + \
    encoded_address + "&lat=" + str(home_lat) + "&lon=" + str(home_lon) + \
    "&wsapikey=" + WALKSCORE_API_KEY
        
    response = requests.get(url).json()
    print(response)
    
    

get_walkscore_info("1119 8th Ave S", "Seattle", "WA", -122.3295 ,47.6085)