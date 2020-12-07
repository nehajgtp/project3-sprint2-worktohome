"""
This file imports infromation from the selected realtor APIs.
(Model)
"""
import os
import json
from os.path import join, dirname
from datetime import datetime
from dotenv import load_dotenv
import googlemaps

import requests
import walkscore_api
import google_maps_api

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
IFRAME_URL = "iframe_url"
COMMUTE_TIME = "commute_time"

HOME_LAT = "home_lat"
HOME_LON = "home_lon"
HOME_WALKSCORE = "home_walkscore"
WALKSCORE_DESCRIPTION = "walkscore_description"
WALKSCORE_LOGO = "walkscore_logo"
WALKSCORE_MORE_INFO_LINK = "walkscore_more_info_link"
HOME_WALKSCORE_LINK = "home_walkscore_link"


def get_homes(city, state_code, min_price, max_price, absolute_address):
    """
    Main Method
    """
    min_price = int(min_price)
    max_price = int(max_price)
    origin_place_id = google_maps_api.get_place_id(absolute_address)
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
        list_of_properties = []
        image = ""
        print(json_body)
        if json_body["meta"]["returned_rows"] != 0:
            for property_instance in json_body["properties"]:
                if "thumbnail" in property_instance:
                    image = property_instance["thumbnail"]
                else:
                    image = "DEFAULT_IMAGE"
                if property_instance["price"] >= min_price and \
                property_instance["price"] <= max_price:
                    pass
                else:
                    continue
                destination_place_id = google_maps_api.get_place_id(
                    property_instance["address"]["line"]
                    + " ,"
                    + property_instance["address"]["city"]
                    + " ,"
                    + property_instance["address"]["state_code"]
                )
                iframe_url = google_maps_api.generate_iframe_url(origin_place_id, destination_place_id)
                now = datetime.now()
                directions_result = GMAPS.directions(
                    absolute_address,
                    property_instance["address"]["line"]
                    + " ,"
                    + property_instance["address"]["city"]
                    + " ,"
                    + property_instance["address"]["state_code"],
                    mode="driving",
                    departure_time=now,
                )
                commute = directions_result[0]["legs"][0]["duration"]["text"]
                walkscore_info = walkscore_api.get_walkscore_info(
                    property_instance["address"]["line"],
                    property_instance["address"]["city"],
                    property_instance["address"]["state_code"],
                    property_instance["address"]["lon"],
                    property_instance["address"]["lat"],
                )
                list_of_properties.append(
                    {
                        HOME_CITY: property_instance["address"]["city"],
                        HOME_STREET: property_instance["address"]["line"],
                        HOME_POSTAL_CODE: property_instance["address"]["postal_code"],
                        HOME_STATE_CODE: property_instance["address"]["state_code"],
                        HOME_STATE: property_instance["address"]["state"],
                        HOME_PRICE: property_instance["price"],
                        HOME_BATHS: property_instance["baths"],
                        HOME_BEDS: property_instance["beds"],
                        HOME_IMAGE: image,
                        HOME_LON: property_instance["address"]["lon"],
                        HOME_LAT: property_instance["address"]["lat"],
                        IFRAME_URL: iframe_url,
                        COMMUTE_TIME: commute,
                        HOME_WALKSCORE: walkscore_info["walkscore"],
                        WALKSCORE_DESCRIPTION: walkscore_info["description"],
                        WALKSCORE_LOGO: walkscore_info["logo"],
                        WALKSCORE_MORE_INFO_LINK: walkscore_info["more_info_link"],
                        HOME_WALKSCORE_LINK: walkscore_info["walkscore_link"],
                    }
                )
            # print(json.dumps(ListOfProperties,indent=2))
            more_properties = nearby_homes(
                property_instance["property_id"], min_price, max_price, absolute_address
            )
            # print(more_properties)
            if more_properties is not None:
                list_of_properties.extend(more_properties)
            # print(json.dumps(list_of_properties, indent=2))

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


def nearby_homes(property_id, min_price, max_price, absolute_address):
    """
    Gets other homes
    """
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
        origin_place_id = google_maps_api.get_place_id(absolute_address)
        for result in results:
            if result["list_price"] >= min_price and result["list_price"] <= max_price:
                geocode_result = GMAPS.geocode(
                    result["location"]["address"]["line"]
                    + result["location"]["address"]["city"]
                )
                destination_place_id = google_maps_api.get_place_id(
                    result["location"]["address"]["line"]
                    + " , "
                    + result["location"]["address"]["city"]
                    + " , "
                    + geocode_result[0]["address_components"][4]["long_name"]
                )
                iframe_url = google_maps_api.generate_iframe_url(origin_place_id, destination_place_id)
                print(iframe_url)
                now = datetime.now()
                directions_result = GMAPS.directions(
                    absolute_address,
                    result["location"]["address"]["line"]
                    + " , "
                    + result["location"]["address"]["city"]
                    + " , "
                    + geocode_result[0]["address_components"][4]["long_name"],
                    mode="driving",
                    departure_time=now,
                )
                commute = directions_result[0]["legs"][0]["duration"]["text"]

                walkscore_info = walkscore_api.get_walkscore_info(
                    result["location"]["address"]["line"],
                    result["location"]["address"]["city"],
                    geocode_result[0]["address_components"][4]["short_name"],
                    geocode_result[0]["geometry"]["location"]["lng"],
                    geocode_result[0]["geometry"]["location"]["lat"],
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
                        HOME_LAT: geocode_result[0]["geometry"]["location"]["lat"],
                        IFRAME_URL: iframe_url,
                        COMMUTE_TIME: commute,
                        HOME_WALKSCORE: walkscore_info["walkscore"],
                        WALKSCORE_DESCRIPTION: walkscore_info["description"],
                        WALKSCORE_LOGO: walkscore_info["logo"],
                        WALKSCORE_MORE_INFO_LINK: walkscore_info["more_info_link"],
                        HOME_WALKSCORE_LINK: walkscore_info["walkscore_link"],
                    }
                )
        # print(json.dumps(list_of_properties_2, indent=2))
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




# getHomes("teaneck","nj",300000,70000000)
# nearbyHomes("M6467862834",300000,10000000)