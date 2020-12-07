import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
import googlemaps
from datetime import datetime

DOTENV_PATH = join(dirname(__file__), "apikeys.env")
load_dotenv(DOTENV_PATH)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GMAPS = googlemaps.Client(key=GOOGLE_API_KEY)

IFRAME_URL = "iframe_url"



def get_place_id(address):
    place = GMAPS.find_place(address,input_type="textquery")
    return place["candidates"][0]["place_id"]

def generate_iframe_url(origin_place_id,destination_place_id):
    url = ("https://www.google.com/maps/embed/v1/directions"
        "?origin=place_id:{}"
        "&destination=place_id:{}"
        "&key={}".format(origin_place_id,destination_place_id,GOOGLE_API_KEY))
    return url
