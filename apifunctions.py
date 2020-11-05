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

def getHomes(city,state_code):
    
    url = "https://rapidapi.p.rapidapi.com/properties/v2/list-for-sale"
    querystring = {"city":city,"limit":"2","offset":"0","state_code":state_code,"sort":"relevance"}
    
    headers = {
    'x-rapidapi-key': rapid_api_key,
    'x-rapidapi-host': "realtor.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_body = response.json()
        ListOfProperties = []
        if json_body["meta"]["returned_rows"] != 0:
            for property in json_body["properties"]:
                ListOfProperties.append(property)
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