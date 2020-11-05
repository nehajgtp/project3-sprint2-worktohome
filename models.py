# models.py
import flask_sqlalchemy
from app import db

LISTINGS = {}

class table_defintion(db.Model):
    address = db.Column(db.String(255), primary_key=True)
    listings = db.Column(db.Array)
    
    def __init__(self, string, price_one, price_two, dist, new_listing):
        search_data = search_parameters(string, price_one, price_two, dist)
        self.address = search_data.address
        LISTINGS.get(search_data.address, new_listing)
        listings = LISTINGS
        
    def __repr__(self):
        return '<The address: %s>' % self.address 

class search_parameters():
    address = ""
    price_range_low = 0
    price_range_high = 0
    distance = 0
    
    def __init__(self, string, price_one, price_two, dist):
        self.address = string;
        self.price_range_low = price_one;
        self.price_range_low = price_two;
        self.distance = dist
        
    def __repr__(self):
        return '<The address is %s, the price is between %d and %d, and the distance is %d.>' % self.address %self.price_range_low %self.price_range_high %self.distance