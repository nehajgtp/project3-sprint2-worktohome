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
import models
import apifunctions

ADDRESSES_RECEIVED_CHANNEL = "addresses received"

APP = flask.Flask(__name__)

SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_APP(APP, cors_allowed_origins="*")

DOTENV_PATH = join(dirname(__file__), "sql.env")
load_dotenv(DOTENV_PATH)

DATABASE_URL = os.environ["DATABASE_URL"]

APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

DB = flask_sqlalchemy.SQLAlchemy(APP)
DB.init_APP(APP)
DB.APP = APP


DB.create_all()
DB.session.commit()

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
    send_to_database(CURRENT_EMAIL, absolute_address, min_price, max_price, distance)
    # listings = apifunctions.getHomes(city, state, min_price, max_price)
    listings = [
        {
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
            "home_lat": 40.8606866,
        }
    ]
    if listings == -1:
        SOCKETIO.emit("sending listing", [])
    else:
        SOCKETIO.emit("sending listing", listings)


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
    return flask.render_template("index.html")


if __name__ == "__main__":
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
