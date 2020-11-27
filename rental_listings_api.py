import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import walkscore_api

DOTENV_PATH = join(dirname(__file__), "apikeys.env")
load_dotenv(DOTENV_PATH)

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

HOME_CITY = "home_city"
HOME_STREET = "home_street"
HOME_POSTAL_CODE = "home_postal_code"
HOME_STATE_CODE = "home_state_code"
HOME_STATE = "home_state"
HOME_COUNTY = "home_county"
HOME_PRICE = "home_price"
HOME_BATHS = "home_baths"
HOME_BEDS = "home_beds"
HOME_IMAGE = "home_image"

HOME_LAT = "home_lat"
HOME_LON = "home_lon"
HOME_WALKSCORE = "home_walkscore"
WALKSCORE_DESCRIPTION = "walkscore_description"
WALKSCORE_LOGO = "walkscore_logo"
WALKSCORE_MORE_INFO_LINK = "walkscore_more_info_link"
HOME_WALKSCORE_LINK = "home_walkscore_link"

def get_rental_listings(city, state_code, min_price, max_price):
    '''
    Main Method
    '''

    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-rent"
    querystring = {
        "city": city,
        "limit": "10",
        "offset": "0",
        "state_code": state_code,
        "sort": "relevance",
        "price_min": min_price,
        "price_max": max_price
    }

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "realtor.p.rapidapi.com",
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_body = response.json()
    # print(json.dumps(json_body, indent=2))
    list_of_properties = []
    image = ""
    try:
        if json_body["meta"]["returned_rows"] > 0:
            for property in json_body["properties"]:
                if property["photo_count"] > 0:
                    image = property["photos"][0]["href"]
                walkscore_info = walkscore_api.get_walkscore_info(property["address"]["line"], property["address"]["city"], \
                        property["address"]["state_code"], property["address"]["lon"], property["address"]["lat"])
                list_of_properties.append(
                    {
                        HOME_CITY: property["address"]["city"],
                        HOME_STREET: property["address"]["line"],
                        HOME_POSTAL_CODE: property["address"]["postal_code"],
                        HOME_STATE_CODE: property["address"]["state_code"],
                        HOME_STATE: property["address"]["state"],
                        HOME_PRICE: property["community"]["price_min"],
                        HOME_BATHS: property["community"]["baths_min"],
                        HOME_BEDS: property["community"]["beds_min"],
                        HOME_IMAGE: image,
                        HOME_LON: property["address"]["lon"],
                        HOME_LAT: property["address"]["lat"],
                        HOME_WALKSCORE: walkscore_info["walkscore"],
                        WALKSCORE_DESCRIPTION: walkscore_info["description"],
                        WALKSCORE_LOGO: walkscore_info["logo"],
                        WALKSCORE_MORE_INFO_LINK: walkscore_info["more_info_link"],
                        HOME_WALKSCORE_LINK: walkscore_info["walkscore_link"]
                    }
                )    
            print(json.dumps(list_of_properties, indent=2))        
        else:
            print("No properties found near this address!")
            return -1
    except requests.exceptions.HTTPError as errh:
        print("getRentalListings API : Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("getRentalListings API : Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("getRentalListings API : Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("getRentalListings API : Something Else", err)
    except IndexError as out_of_bound:
        print("No results found for this address!")
        
get_rental_listings("New York", "NY", "20", "2000")