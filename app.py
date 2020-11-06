# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 

ADDRESSES_RECEIVED_CHANNEL = 'addresses received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

CURRENT_EMAIL = ""

#CALL THIS FUNCTION TO ADD TO THE DATABASE OR UPDATE DATABASE
def sendToDatabase(email, address, price_range_low, price_range_high, distance, listing):
    if(db.query()):#Has the table
       z = 0 #TODO Update the record
    else:#Doesn't have the table
        db.session.add(models.table_defintion(address, price_range_low, price_range_high, distance, listing))
        db.session.commit()
    return None # !!!!!!!
def displayTable(user_email):
    if db.seesion.query(): #TODO find a table matching the user
        socketio.emit("current table", {})
    else: #Didn't find it.
        socketio.emit("current table", {})
    return None #!!!!

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('send search parameters')
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
    #return ?
    
@app.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
