import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import walkscore_api
import googlemaps
from datetime import datetime

from google_maps_api import get_place_id, generate_iframe_url

DOTENV_PATH = join(dirname(__file__), "apikeys.env")
load_dotenv(DOTENV_PATH)

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GMAPS = googlemaps.Client(key=GOOGLE_API_KEY)


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
IFRAME_URL = "iframe_url"
COMMUTE_TIME = "commute_time"

HOME_LAT = "home_lat"
HOME_LON = "home_lon"
HOME_WALKSCORE = "home_walkscore"
WALKSCORE_DESCRIPTION = "walkscore_description"
WALKSCORE_LOGO = "walkscore_logo"
WALKSCORE_MORE_INFO_LINK = "walkscore_more_info_link"
HOME_WALKSCORE_LINK = "home_walkscore_link"

def get_rental_listings(city, state_code, min_price, max_price, absolute_address):
    '''
    Main Method
    '''
    origin_place_id = get_place_id(absolute_address)
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
    home_price = ""
    home_baths = ""
    home_beds = ""
    
    try:
        if json_body["meta"]["returned_rows"] > 0:
            for property in json_body["properties"]:
                print(property)
                if property["photo_count"] > 0:
                    image = property["photos"][0]["href"]
                key = "community"
                if key in property:
                    home_price = property[key]["price_min"]
                    home_baths = property[key]["baths_min"]
                    home_beds = property[key]["beds_min"]
                if key not in property:
                    home_price = property["price"]
                    home_baths = property["baths"]
                    home_beds = property["beds"]
                destination_place_id = get_place_id(property["address"]["line"] + 
                " ," + property["address"]["city"] + " ,"+ property["address"]["state_code"])
                iframe_url = generate_iframe_url(origin_place_id,destination_place_id)
                now = datetime.now()
                directions_result = GMAPS.directions(absolute_address,
                                     property["address"]["line"] + \
                                     " ," + property["address"]["city"] + " ," \
                                     + property["address"]["state_code"],
                                     mode="driving",
                                     departure_time=now)
                commute = directions_result[0]["legs"][0]["duration"]["text"]
                walkscore_info = walkscore_api.get_walkscore_info(property["address"]["line"], property["address"]["city"], property["address"]["state_code"], property["address"]["lon"], property["address"]["lat"])
                list_of_properties.append(
                    {
                        HOME_CITY: property["address"]["city"],
                        HOME_STREET: property["address"]["line"],
                        HOME_POSTAL_CODE: property["address"]["postal_code"],
                        HOME_STATE_CODE: property["address"]["state_code"],
                        HOME_STATE: property["address"]["state"],
                        HOME_PRICE: home_price,
                        HOME_BATHS: home_baths,
                        HOME_BEDS: home_beds,
                        HOME_IMAGE: image,
                        HOME_LON: property["address"]["lon"],
                        HOME_LAT: property["address"]["lat"],
                        IFRAME_URL : iframe_url,
                        COMMUTE_TIME : commute,
                        HOME_WALKSCORE: walkscore_info["walkscore"],
                        WALKSCORE_DESCRIPTION: walkscore_info["description"],
                        WALKSCORE_LOGO: walkscore_info["logo"],
                        WALKSCORE_MORE_INFO_LINK: walkscore_info["more_info_link"],
                        HOME_WALKSCORE_LINK: walkscore_info["walkscore_link"]
                    }
                )    
            # print(json.dumps(list_of_properties, indent=2))   
            return list_of_properties
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
    except KeyError as errk:
        print("KeyError", errk)
        
