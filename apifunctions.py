import requests
import json
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), 'apikeys.env')
load_dotenv(dotenv_path)

null = None
false = False
true = True
rapid_api_key = os.environ["RAPID_API_KEY"]

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


def getHomes(city,state_code,min_price,max_price):
    
    url = "https://rapidapi.p.rapidapi.com/properties/v2/list-for-sale"
    querystring = {"city":city,"limit":"8","offset":"0","state_code":state_code,"sort":"relevance"}
    
    headers = {
    'x-rapidapi-key': rapid_api_key,
    'x-rapidapi-host': "realtor.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_body = response.json()
        ListOfProperties = []
        image = ""
        if json_body["meta"]["returned_rows"] != 0:
            for property in json_body["properties"]:
                if "thumbnail"  in property:
                    image = property["thumbnail"]
                else:
                    image = "DEFAULT_IMAGE"
                if property["price"] >= min_price and property["price"] <= max_price:
                    pass
                else:
                    continue
                ListOfProperties.append({
                    HOME_CITY: property["address"]["city"],
                    HOME_STREET: property["address"]["line"],
                    HOME_POSTAL_CODE:property["address"]["postal_code"],
                    HOME_STATE_CODE:property["address"]["state_code"],
                    HOME_STATE:property["address"]["state"],
                    HOME_COUNTY:property["address"]["county"],
                    HOME_PRICE:property["price"],
                    HOME_BATHS:property["baths"],
                    HOME_BEDS:property["beds"],
                    HOME_IMAGE:image,
                    HOME_LON:property["address"]["lon"],
                    HOME_LAT:property["address"]["lat"]
                })
            print(json.dumps(ListOfProperties,indent=2))
            return ListOfProperties
        else:
            print("No properties found near this address!")
            return -1
    except requests.exceptions.HTTPError as errh:
        print ("getHomes API : Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("getHomes API : Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("getHomes API : Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("getHomes API : Something Else",err)
    except IndexError as e:
        print("No results found for this address!")

        
        
getHomes("clifton","nj",500000,700000)
