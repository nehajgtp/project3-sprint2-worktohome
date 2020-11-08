# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
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
DB.init_app(app)
DB.app = app


DB.create_all()
DB.session.commit()

CURRENT_EMAIL = ""

#CALL THIS FUNCTION TO ADD TO THE DATABASE OR UPDATE DATABASE
def sendToDatabase(email, address, price_range_low, price_range_high, distance, listing):
    records = DB.query(models.table_defintion).all()
    if(records != None):#Has the table
        DB.session.update()
    else:#Doesn't have the table
        DB.session.add(models.table_defintion(address, price_range_low, price_range_high, distance, listing))
        DB.session.commit()
    return None # !!!!!!!
    
def displayTable(user_email):#For Sprint 2
    if DB.seesion.query(): #TODO find a table matching the user
        SOCKETIO.emit("current table", {})
    else: #Didn't find it.
        SOCKETIO.emit("current table", {})
    return None #!!!!

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
    email = data["email"]
    CURRENT_EMAIL = email

    
@SOCKETIO.on('send search parameters')
def parsing_search_parameters(data):
    street_address = data["address"]
    city = data["city"]
    state = data["state"]
    distance = data["max_communte"]
    min_price = data["min_price"]
    max_price = data["max_price"]
    absolute_address = street_address + ", " + city + ", " + state 
    listing = None # CALL API HERE
    sendToDatabase(CURRENT_EMAIL, absolute_address, min_price, max_price, distance, listing)
    listings = apifunctions.getHomes(city, state, min_price, max_price)
    if(listings == -1):
        return None
    else:
        send_listings(listings)
    #return ?
    
def send_listings(array):
    #for listing in array:
    SOCKETIO.emit('sending listings', array)

    
@app.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == '__main__': 
    SOCKETIO.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
