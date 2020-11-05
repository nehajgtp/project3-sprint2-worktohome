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

