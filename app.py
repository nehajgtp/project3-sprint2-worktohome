# APP.py
'''
The file handles the inputs and outputs
'''
import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_sqlalchemy
import flask_socketio
import apifunctions

ADDRESSES_RECEIVED_CHANNEL = "addresses received"

APP = flask.Flask(__name__)

SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

DOTENV_PATH = join(dirname(__file__), "sql.env")
load_dotenv(DOTENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

DB = flask_sqlalchemy.SQLAlchemy(APP)
def init_db(app):
    '''
    Initialize the database
    '''
    DB.init_app(app)
    DB.app = app
    DB.create_all()
    DB.session.commit()

import models
CURRENT_EMAIL = ""

def send_to_database(email, address, price_range_low, price_range_high, distance):
    '''
    CALL THIS FUNCTION TO ADD TO THE DATABASE OR UPDATE DATABASE
    '''
    DB.session.add(
        models.TableDefintion(
            email, address, price_range_low, price_range_high, distance
        )
    )
    DB.session.commit()


def display_table():
    '''
    For Sprint 2
    '''
    records = (
        DB.session.query(models.TableDefintion)
        .filter(models.TableDefintion.email == CURRENT_EMAIL)
        .all()
    )
    if records is not None:
        history_table = []
        for record in records:
            history_table.append(record)
        SOCKETIO.emit("current table", history_table)
    else:  # Didn't find it.
        SOCKETIO.emit("current table", [])


@SOCKETIO.on("connect")
def on_connect():
    '''
    Startup of the frontend
    '''
    print("Someone connected!")
    SOCKETIO.emit("connected", {"test": "Connected"})


@SOCKETIO.on("disconnect")
def on_disconnect():
    '''
    Closing the tab
    '''
    print("Someone disconnected!")


@SOCKETIO.on("New Logged In User")
def new_user(data):
    '''
    ...
    '''
    global CURRENT_EMAIL
    email = data["email"]
    CURRENT_EMAIL = email


@SOCKETIO.on("send search parameters")
def parsing_search_parameters(data):
    '''
    Main Function
    '''
    street_address = data["address"]
    city = data["city"]
    state = data["state"]
    distance = data["max_commute"]
    min_price = data["min_price"]
    max_price = data["max_price"]
    absolute_address = street_address + ", " + city + ", " + state
    
    invalid_input_errors = []
    if (min_price < 0):
        invalid_input_errors.append("The min price cannot be a negative number")
    if (max_price < 0):
        invalid_input_errors.append("The max price cannot be a negative number")
    
    if (min_price > max_price):
        invalid_input_errors.append("Min price cannot be bigger than max price")
    
    if (len(invalid_input_errors) == 0): 
        send_to_database(CURRENT_EMAIL, absolute_address, min_price, max_price, distance)
        listings = apifunctions.get_homes(city, state, min_price, max_price)
        print(listings)
        if listings == -1:
            SOCKETIO.emit('sending listing', [])
        else:
            SOCKETIO.emit("sending listing", listings)
    if (len(invalid_input_errors) > 0):
        SOCKETIO.emit('Invalid search input', invalid_input_errors)
        print("Errors sent")
        print(invalid_input_errors)
        invalid_input_errors = []


@APP.route("/")
def index():
    '''
    Basic Frontend
    '''
    return flask.render_template("index.html")


@APP.route("/content")
def content():
    '''
    Kevin's Frontend
    '''
    init_db(APP)
    return flask.render_template("index.html")


if __name__ == '__main__':
    init_db(APP)
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
