# models.py
import flask_sqlalchemy
from app import DB

class table_defintion(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)   
    email = DB.Column(DB.String(255))
    address = DB.Column(DB.String(255))
    price_low = DB.Column(DB.Integer)
    price_high = DB.Column(DB.Integer)
    distance = DB.Column(DB.Integer)

    def __init__(self, email, address, price_one, price_two, dist):
        search_data = search_parameters(address, price_one, price_two, dist)
        self.email = email
        self.address = search_data.address
        self.price_low = search_data.price_range_low
        self.price_high = search_data.price_range_high
        self.distance = search_data.distance

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