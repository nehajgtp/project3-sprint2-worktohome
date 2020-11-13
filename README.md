# Project 3 - MVP (Work to Home)
Make your home search more convenient to your commute!

## Setting up React and PSQL
> React
0.  `cd ~/environment && git clone https://github.com/Sresht/lect11/ && cd lect11`
1.  Install your stuff!  
    a)  `npm install`  
    b)  `pip install flask-socketio`  
    c)  `pip install eventlet`  
    d)  `npm install -g webpack`  
    e)  `npm install --save-dev webpack`  
    f)  `npm install socket.io-client --save` 
    g) `pip install googlemaps`
    If you see any error messages, make sure you use  `sudo pip`  or  `sudo npm`. If it says "pip cannot be found", run  `which pip`  and use  `sudo [path to pip from which pip] install`

> Getting PSQL to work with Python

1.  Update yum:  `sudo yum update`, and enter yes to all prompts
2.  Upgrade pip:  `sudo /usr/local/bin/pip install --upgrade pip`
3.  Get psycopg2:  `sudo /usr/local/bin/pip install psycopg2-binary`
4.  Get SQLAlchemy:  `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`

> PSQL

1.  Install PostGreSQL:  `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`  
    Enter yes to all prompts.
2.  Initialize PSQL database:  `sudo service postgresql initdb`
3.  Start PSQL:  `sudo service postgresql start`
4.  Make a new superuser:  `sudo -u postgres createuser --superuser $USER`  
    If you get an error saying "could not change directory", that's okay! It worked!
5.  Make a new database:  `sudo -u postgres createdb $USER`  
    If you get an error saying "could not change directory", that's okay! It worked!
6.  Make sure your user shows up:  
    a)  `psql`  
    b)  `\du`  look for ec2-user as a user  
    c)  `\l`  look for ec2-user as a database
7.  Make a new user:  
    a)  `psql`  (if you already quit out of psql)
    b) I recommend 4-5 characters - it doesn't have to be very secure. Remember this password!  
    `create user [some_username_here] superuser password '[some_unique_new_password_here]';`  
    c)  `\q`  to quit out of sql
8.  `cd`  into  `lect11`  and make a new file called  `sql.env`  and add  `SQL_USER=`  and  `SQL_PASSWORD=`  in it
9.  Fill in those values with the values you put in 7. b)

## Setting up API Keys
> Setting up Rapid API
1. Go to https://rapidapi.com/marketplace and create an account (preferably use Github account to create new account).
2. Once new account is created, go to https://rapidapi.com/apidojo/api/realtor and copy the API key in `X-RapidAPI-Key` to clipboard.
> Setting up Python Client for Google Maps
3. Create a Google account or login to your current Google account.
4. Go to https://console.cloud.google.com/apis/credentials
5. Click  "Create Credentials" and click on "API Key".
6. Copy API key for the Google API key.
> Create file for API Keys
7. Run `cd project3-worktohome && touch apikeys.env`
8. Open the `apikeys.env` file and enter the following:

    RAPID_API_KEY='YOUR_RAPID_API_KEY'
    GOOGLE_API_KEY='YOUR_GOOGLE_API_KEY'

## Enabling read/write from SQLAlchemy

There's a special file that you need to enable your db admin password to work for:

1.  Open the file in vim:  `sudo vim /var/lib/pgsql9/data/pg_hba.conf`  If that doesn't work:  `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`
2.  Replace all values of  `ident`  with  `md5`  in Vim:  `:%s/ident/md5/g`
3.  After changing those lines, run  `sudo service postgresql restart`
4.  Ensure that  `sql.env`  has the username/password of the superuser you created!
5.  Run your code!  
    a)  `npm run watch`. If prompted to install webpack-cli, type "yes"  
    b) In a new terminal,  `python app.py`  
    c) Preview Running Application (might have to clear your cache by doing a hard refresh)

