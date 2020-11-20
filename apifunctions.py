'''
This file imports infromation from the selected APIs.
'''
import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
import googlemaps
from datetime import datetime
import requests
import walkscore_api

DOTENV_PATH = join(dirname(__file__), "apikeys.env")
load_dotenv(DOTENV_PATH)

NULL = None
FALSE = False
TRUE = True
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

HOME_LAT = "home_lat"
HOME_LON = "home_lon"
HOME_WALKSCORE = "home_walkscore"


def get_homes(city, state_code, min_price, max_price):
    '''
    Main Method
    '''
    min_price = int(min_price)
    max_price = int(max_price)
    url = "https://rapidapi.p.rapidapi.com/properties/v2/list-for-sale"
    querystring = {
        "city": city,
        "limit": "5",
        "offset": "0",
        "state_code": state_code,
        "sort": "relevance",
    }

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "realtor.p.rapidapi.com",
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_body = response.json()
        # print(json.dumps(json_body,indent=2))
        list_of_properties = []
        image = ""
        #county = "county"
        if json_body["meta"]["returned_rows"] != 0:
            for property in json_body["properties"]:
                if "thumbnail" in property:
                    image = property["thumbnail"]
                else:
                    image = "DEFAULT_IMAGE"
                if property["price"] >= min_price and property["price"] <= max_price:
                    pass
                else:
                    continue
                list_of_properties.append(
                    {
                        HOME_CITY: property["address"]["city"],
                        HOME_STREET: property["address"]["line"],
                        HOME_POSTAL_CODE: property["address"]["postal_code"],
                        HOME_STATE_CODE: property["address"]["state_code"],
                        HOME_STATE: property["address"]["state"],
                        HOME_PRICE: property["price"],
                        HOME_BATHS: property["baths"],
                        HOME_BEDS: property["beds"],
                        HOME_IMAGE: image,
                        HOME_LON: property["address"]["lon"],
                        HOME_LAT: property["address"]["lat"],
                        HOME_WALKSCORE: walkscore_api.get_walkscore_info(property["address"]["line"], property["address"]["city"], \
                        property["address"]["state_code"], property["address"]["lon"], property["address"]["lat"])
                    }
                )
            # print(json.dumps(ListOfProperties,indent=2))
            more_properties = nearby_homes(property["property_id"], min_price, max_price)
            print(more_properties)
            if more_properties is not None:
                list_of_properties.extend(more_properties)
            print(json.dumps(list_of_properties, indent=2))

        else:
            print("No properties found near this address!")
            return -1
        return list_of_properties
    except requests.exceptions.HTTPError as errh:
        print("getHomes API : Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("getHomes API : Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("getHomes API : Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("getHomes API : Something Else", err)
    except IndexError as out_of_bound:
        print("No results found for this address!")


def nearby_homes(property_id, min_price, max_price):
    '''
    Gets other homes
    '''
    url = "https://realtor.p.rapidapi.com/properties/v2/list-similar-homes"
    querystring = {"property_id": property_id}

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "realtor.p.rapidapi.com",
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_body = response.json()
        results = json_body["data"]["home"]["related_homes"]["results"]
        list_of_properties_2 = []
        for result in results:
            if result["list_price"] >= min_price and result["list_price"] <= max_price:
                geocode_result = GMAPS.geocode(
                    result["location"]["address"]["line"]
                    + result["location"]["address"]["city"]
                )

                list_of_properties_2.append(
                    {
                        HOME_CITY: result["location"]["address"]["city"],
                        HOME_STREET: result["location"]["address"]["line"],
                        HOME_POSTAL_CODE: geocode_result[0]["address_components"][6][
                            "long_name"
                        ],
                        HOME_STATE_CODE: geocode_result[0]["address_components"][4][
                            "short_name"
                        ],
                        HOME_STATE: geocode_result[0]["address_components"][4][
                            "long_name"
                        ],
                        HOME_COUNTY: geocode_result[0]["address_components"][3][
                            "long_name"
                        ],
                        HOME_PRICE: result["list_price"],
                        HOME_BATHS: result["description"]["baths"],
                        HOME_BEDS: result["description"]["beds"],
                        HOME_IMAGE: result["primary_photo"]["href"],
                        HOME_LON: geocode_result[0]["geometry"]["location"]["lng"],
                        HOME_LAT:geocode_result[0]["geometry"]["location"]["lat"],
                        HOME_WALKSCORE: walkscore_api.get_walkscore_info(result["location"]["address"]["line"], result["location"]["address"]["city"], \
                        geocode_result[0]["address_components"][4]["short_name"], geocode_result[0]["geometry"]["location"]["lng"], \
                        geocode_result[0]["geometry"]["location"]["lat"])
                    })
        print(json.dumps(list_of_properties_2, indent=2))
        return list_of_properties_2
    except requests.exceptions.HTTPError as errh:
        print("getHomes API : Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("getHomes API : Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("getHomes API : Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("getHomes API : Something Else", err)
    except IndexError as out_of_bound:
        print("nearby: No results found for this address!")

def get_distance(start_address, end_address):
    '''
    Calculates distance with GMAPS
    '''
    now = datetime.now()
    directions_result = GMAPS.directions(
        start_address, end_address, mode="driving", departure_time=now
    )
    print(json.dumps(directions_result, indent=2))


# getHomes("teaneck","nj",300000,70000000)
# nearbyHomes("M6467862834",300000,10000000)
