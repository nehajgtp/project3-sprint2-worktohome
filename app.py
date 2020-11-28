# APP.py
"""
The file handles the inputs and outputs
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_sqlalchemy
import flask_socketio
import apifunctions
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


def send_to_database(email, address, price_range_low, price_range_high, distance):
    """
    CALL THIS FUNCTION TO ADD TO THE DATABASE OR UPDATE DATABASE
    """
    DB.session.add(
        models.TableDefintion(
            email, address, price_range_low, price_range_high, distance
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
    send_to_database(EMAIL_CLASS.value_of(), absolute_address, min_price, max_price, distance)
    listings = apifunctions.get_homes(city, state, min_price, max_price)
    if listings == -1:
        SOCKETIO.emit("sending listing", [])
    else:
        SOCKETIO.emit("sending listing", listings)


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
