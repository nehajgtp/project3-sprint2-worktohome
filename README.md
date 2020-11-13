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

## Linting
### app.py
    app.py:34:0: C0413: Import "import models" should be placed at the top of the module (wrong-import-position) : Needs to be in this location to prevent an error according to Kevin.
    app.py:54:8: E1101: Instance of 'query' has no 'filter' member (no-member) : Pylint doesn't detect the method member.
    app.py:89:4: W0603: Using the global statement (global-statement) : Would need an entire overhaul of the email handling to solve.
    app.py:137:17: W1508: os.getenv default type is builtins.int. Expected str or None. (invalid-envvar-default) : It is correct ignore this error. 

### models.py
    models.py:20:4: R0913: Too many arguments (6/5) (too-many-arguments) : It's really close to the max number of arguments and would require a massive overhaul of the application.
    models.py:9:0: R0903: Too few public methods (1/2) (too-few-public-methods) : Unnecessary to add more methods
    models.py:32:0: R0903: Too few public methods (1/2) (too-few-public-methods) : Unnecessary to add more methods
    models.py:5:0: W0611: Unused import flask_sqlalchemy (unused-import) : Import is actually nesscary to prevent werid behavior, pylint just does not know this.

### apifunctions.py
    apifunctions.py:66:16: W0622: Redefining built-in 'property' (redefined-builtin): Ali's code.
    apifunctions.py:39:0: R0914: Too many local variables (18/15) (too-many-locals) : Ali's code would require a large refactor.
    apifunctions.py:91:43: W0631: Using possibly undefined loop variable 'property' (undefined-loop-variable) : It is defined. 
    apifunctions.py:109:4: W0612: Unused variable 'out_of_bound' (unused-variable) : Describes the error
    apifunctions.py:39:0: R0912: Too many branches (13/12) (too-many-branches) : Ali's code would require a large refactor.
    apifunctions.py:113:0: R0914: Too many local variables (17/15) (too-many-locals) : Ali's code would require a large refactor.
    apifunctions.py:169:4: W0612: Unused variable 'out_of_bound' (unused-variable) : Describes the error
    apifunctions.py:9:0: C0411: standard import "from datetime import datetime" should be placed before "from dotenv import load_dotenv" (wrong-import-order)

## In Terminal
    Must run this if psql is not running: sudo service postgresql start
    Than must source API keys.
    Run python app.py
