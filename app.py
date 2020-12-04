# APP.py
"""
The file handles the inputs and outputs. (Controller)
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_sqlalchemy
import flask_socketio
import apifunctions
import rental_listings_api
import email_file

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
    """
    Initialize the database
    """
    DB.init_app(app)
    DB.app = app
    DB.create_all()
    DB.session.commit()


import models

EMAIL_CLASS = email_file.Email("")


def send_to_database(email, address, price_range_low, price_range_high, distance, city, state, purchase_type):
    """
    CALL THIS FUNCTION TO ADD TO THE DATABASE OR UPDATE DATABASE
    """
    DB.session.add(
        models.TableDefintion(
            email, address, price_range_low, price_range_high, distance,\
            city, state, purchase_type\
        )
    )
    DB.session.commit()


@SOCKETIO.on("request search history")
def display_table():
    """
    For Sprint 2
    """
    records = (
        DB.session.query(models.TableDefintion)
        .filter(models.TableDefintion.email == EMAIL_CLASS.value_of())
        .all()
    )
    if records is not None:
        history_table = []
        for record in records:
            transfer = {
                "address": record.address,
                "price_low": record.price_low,
                "price_high": record.price_high,
                "distance": record.distance,
            }
            history_table.append(transfer)
        print(history_table)
        SOCKETIO.emit("received database info", history_table)
    else:  # Didn't find it.
        SOCKETIO.emit("received database info", [])


@SOCKETIO.on("connect")
def on_connect():
    """
    Startup of the frontend
    """
    # print("Someone connected!")
    SOCKETIO.emit("connected", {"test": "Connected"})


@SOCKETIO.on("disconnect")
def on_disconnect():
    """
    Closing the tab
    """
    # print("Someone disconnected!")


@SOCKETIO.on("New Logged In User")
def new_user(data):
    """
    ...
    """
    email_variable = data["email"]
    EMAIL_CLASS.set_email(email_variable)


@SOCKETIO.on("send search parameters")
def parsing_search_parameters(data):
    """
    Main Function
    """
    street_address = data["address"]
    city = data["city"]
    state = data["state"]
    distance = data["max_commute"]
    min_price = data["min_price"]
    max_price = data["max_price"]
    absolute_address = street_address + ", " + city + ", " + state
    purchase_type = data["purchase_type"]

    print(data)
    invalid_input_errors = []
    if min_price < 0:
        invalid_input_errors.append("The min price cannot be a negative number")
    if max_price < 0:
        invalid_input_errors.append("The max price cannot be a negative number")

    if min_price > max_price:
        invalid_input_errors.append("Min price cannot be bigger than max price")

    if len(invalid_input_errors) == 0:
        send_to_database(
            EMAIL_CLASS.value_of(), absolute_address, min_price, max_price,\
            distance, city, state, purchase_type\
        )
        listings = ""
        if purchase_type == "sale":
            y = 0
            #listings = apifunctions.get_homes(
            #    city, state, min_price, max_price, absolute_address
            #)
        if purchase_type == "rent":
            x = 0
            #listings = rental_listings_api.get_rental_listings(
            #    city, state, str(min_price), str(max_price)
            #)
        listing = [  {
        "home_city": "Morris Plains",
        "home_street": "14 Rita Dr",
        "home_postal_code": "07950",
        "home_state_code": "NJ",
        "home_state": "New Jersey",
        "home_county": "Morris County",
        "home_price": 494900,
        "home_baths": 2,
        "home_beds": 3,
        "home_image": "https://ap.rdcpix.com/4f5171535d64d87096aca43b6b9035e4l-m1056436147xd-w300_h300_q80.jpg",
        "home_lon": -74.4537076,
        "home_lat": 40.8606866
        } ]
        print(listings)
        if listings == -1:
            SOCKETIO.emit("sending listing", [])
        else:
            SOCKETIO.emit("sending listing", listings)
    if len(invalid_input_errors) > 0:
        SOCKETIO.emit("Invalid search input", invalid_input_errors)
        print("Errors sent")
        print(invalid_input_errors)
        invalid_input_errors = []


@SOCKETIO.on("sort listings")
def sort_listings(listings):
    '''
    Solution to handling change in desired list order
    '''
    SOCKETIO.emit("sorted listings", listings)


@APP.route("/")
def index():
    """
    Basic Frontend
    """
    return flask.render_template("index.html")


@APP.route("/content")
def content():
    """
    Kevin's Frontend
    """
    return flask.render_template("index.html")


@APP.route("/history")
def history():
    """
    Matt's Frontend
    """
    return flask.render_template("index.html")


if __name__ == "__main__":
    init_db(APP)
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
