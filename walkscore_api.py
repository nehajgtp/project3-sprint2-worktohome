"""
This file handles data from the Walkscore API. (model)
"""
import os
import urllib
from os.path import join, dirname
from dotenv import load_dotenv
import requests

DOTENV_PATH = join(dirname(__file__), "apikeys.env")
load_dotenv(DOTENV_PATH)

WALKSCORE_API_KEY = os.getenv("WALKSCORE_API_KEY")


def get_walkscore_info(home_street, home_city, home_state_code, home_lon, home_lat):
    """
    Main Function
    """
    try:
        address = home_street + " " + home_city + " " + home_state_code
        encoded_address = urllib.parse.quote_plus(address)

        url = (
            "https://api.walkscore.com/score?format=json&address="
            + encoded_address
            + "&lat="
            + str(home_lat)
            + "&lon="
            + str(home_lon)
            + "&wsapikey="
            + WALKSCORE_API_KEY
        )

        response = requests.get(url).json()

        walkscore_info = {
            "walkscore": response["walkscore"],
            "description": response["description"],
            "logo": response["logo_url"],
            "more_info_link": response["more_info_link"],
            "walkscore_link": response["ws_link"],
        }

        return walkscore_info
    except requests.exceptions.HTTPError as errh:
        print("Walkscore API : Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Walkscore API : Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Walkscore API : Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Walkscore API : Something Else", err)
    except IndexError as out_of_bound:
        print("Walkscore API: No results found for this address!")
