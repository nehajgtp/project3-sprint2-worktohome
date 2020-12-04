# models.py
'''
Defines the table for PSQL (Model)
'''
import flask_sqlalchemy
from app import DB

class TableDefintion(DB.Model):
    '''
    Main class
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(255))
    address = DB.Column(DB.String(255))
    price_low = DB.Column(DB.Integer)
    price_high = DB.Column(DB.Integer)
    distance = DB.Column(DB.Integer)
    city = DB.Column(DB.String(60))
    state = DB.Column(DB.String(60))
    purchase_type = DB.Column(DB.String(60))

    def __init__(self, email, address, price_one, price_two, dist, city, state, purchase_type):
        self.email = email
        self.address = address
        self.price_low = price_one
        self.price_high = price_two
        self.distance = dist
        self.city = city
        self.state = state
        self.purchase = purchase_type

    def __repr__(self):
        return (
            "<The address is %s, the price is between %d and %d, and the distance is %d.>"
            % self.address
            % self.price_range_low
            % self.price_range_high
            % self.distance
        )
