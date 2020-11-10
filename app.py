# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import apifunctions

ADDRESSES_RECEIVED_CHANNEL = 'addresses received'

app = flask.Flask(__name__)

SOCKETIO = flask_socketio.SocketIO(app)
SOCKETIO.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

DB = flask_sqlalchemy.SQLAlchemy(app)
def init_db(app):
    DB.init_app(app)
    DB.app = app
    DB.create_all()
    DB.session.commit()

import models
CURRENT_EMAIL = ""

#CALL THIS FUNCTION TO ADD TO THE DATABASE OR UPDATE DATABASE
def sendToDatabase(email, address, price_range_low, price_range_high, distance):
    DB.session.add(models.table_defintion(CURRENT_EMAIL, address, price_range_low, price_range_high, distance))
    DB.session.commit()
    
def displayTable(user_email):#For Sprint 2
    
    records = DB.session.query(models.table_defintion).filter(models.table_defintion.email == CURRENT_EMAIL).all()
    if records != None: #TODO find a table matching the user
        history_table = []
        for record in records:
            history_table.append(record)
        SOCKETIO.emit("current table", history_table)
    else: #Didn't find it.
        SOCKETIO.emit("current table", [])

@SOCKETIO.on('connect')
def on_connect():
    print('Someone connected!')
    SOCKETIO.emit('connected', {
        'test': 'Connected'
    })
    
@SOCKETIO.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@SOCKETIO.on('New Logged In User')
def new_user(data):
    global CURRENT_EMAIL
    email = data["email"]
    CURRENT_EMAIL = email

    
@SOCKETIO.on('send search parameters')
def parsing_search_parameters(data):
    street_address = data["address"]
    city = data["city"]
    state = data["state"]
    distance = data["max_commute"]
    min_price = data["min_price"]
    max_price = data["max_price"]
    absolute_address = street_address + ", " + city + ", " + state 
    listing = None # CALL API HERE
    sendToDatabase(CURRENT_EMAIL, absolute_address, min_price, max_price, distance)
    listings = apifunctions.getHomes(city, state, min_price, max_price)
    print(listings)
    if(listings == -1):
        SOCKETIO.emit('sending listing', [])
    else:
        SOCKETIO.emit('sending listing', listings)

    
@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/content')
def content():
    init_db(app)
    return flask.render_template("index.html")


if __name__ == '__main__': 
    SOCKETIO.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
