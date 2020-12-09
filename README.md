# Work to Home (Sprint 2)
Make your home search more convenient to your commute!

https://worktohome-sprint2.herokuapp.com/

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
    g)  `pip install googlemaps`
    h)  `npm install react-router-dom`
    i)  `npm install react-facebook-login`
    k)  `npm install react-spinners`
    l)  `npm install style-loader css-loader --save`
    m)  `npm i react-iframe`
    n)  `npm install —save @material-ui/core`
    o)  `npm install react-number-format --save`
    p)  `npm install --save prop-types`
    q)  `pip install mock`
    r)  `pip install python-dotenv`
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

## Google Login OAUTH
1. run `npm install react-google-login`
2. Go to https://console.developers.google.com and sign up with personal google account
3. Click "CREATE PROJECT" or in "Select a Project", click "New Project"
4. Name your project.
5. Click "Credentials" and then click "Create Credentials" and click "OAuth client ID"
6. If you see a warning, saying "To create an OAuth client ID, you must first set...", do these steps\
    a) Click "CONFIGURE CONSENT SCREEN"
    b) Choose "External"
    c) Give the application a name and press save.
5. Go to Credentials -> Create Credentials -> OAuth client ID and click "web application"
6. Put the URL of the web app in Authorized JavaScript origins and Authorized redirect URIs\
7. Put your client id in the GoogleButton.jsx file under the scripts folder.

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
9. Install googlemaps dependency  ``` pip install -U googlemaps ```

> Setting up Walkscore API
  1. Go to [this](https://www.walkscore.com/professional/api-sign-up.php) link.
  2. Sign up with your information.
  3. When you receive your API Key in an email from Walkscore, add the key to the `apikeys.env` file as `WALKSCORE_API_KEY='YOUR_API_KEY'`

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

## Unit Testing
1. run `pip install coverage`
2. To run all tests, run `coverage run -m --source=. unittest testing/*.py`

## Heroku Deployment
1. Go to heroku.com and make an account
2. Run `npm install -g heroku` for heroku installation
3. Run the following commands (enter login when prompted to do so):
    a)`heroku login -i`
    b) `heroku create`
    c) `heroku addons:create heroku-postgresql:hobby-dev`
    d) `heroku pg:wait`
4. Alter Users
    e) `sudo service postgresql start`
    d) `psql`
    f) `ALTER DATABASE Postgres OWNER TO <your_psql_username>`
    g) `ALTER USER <your_psql_username> WITH CREATEDB CREATEROLE REPLICATION`
    h) `\du`
    i) `\l`
    j) `\q`
5. Push Database to Heroku
    k) `heroku pg:push postgres DATABASE_URL`
    l) `heroku pg:psql`
    m) `select * from message;`
    n) `\q` to exit
6. add the changes to git
7. `touch Procfile && touch requirements.txt`
8. `pip freeze > requirements.txt`
9. `echo "web: python app.py" > Procfile`
10. add and commit Procfile and requiremnts.txt
11. run `npm run build`
11. push to master
12. run `git push heroku master`
13. Check your heroku link to see the deployment!
14. Make sure to add your GOOGLE_API_KEY and RAPID_API_KEY to config variables

### CircleCI:
1. Go to https://circleci.com/signup/ and sign up with your github account
2. Authorize and verify the account
3. Make sure you're in the right repo and organization
4. Click on the project and specify that are you're using an existing cirlce config.
5. The one for this project is inside .circleci and claled `config.yml`
6. Go to project settings -> environment variables
7. Create environment variables for HEROKU_API_KEY and HEROKU_APP_NAME, you should \
   be able to find the key in your heroku account.
8. Add environment variables for GOOGLE_API_KEY and HEROKU_APP_NAME
9. Now pushing should start a new build and deploy process
10. If you run into an issue during building with circlci, run `pip freeze > requirements.txt`

## Linting
### app.py
    app.py:34:0: C0413: Import "import models" should be placed at the top of the module (wrong-import-position) : Needs to be in this location to prevent an error according to Kevin.
    app.py:54:8: E1101: Instance of 'query' has no 'filter' member (no-member) : Pylint doesn't detect the method member.
    app.py:137:17: W1508: os.getenv default type is builtins.int. Expected str or None. (invalid-envvar-default) : It is correct ignore this error. 

### models.py
    models.py:20:4: R0913: Too many arguments (6/5) (too-many-arguments) : It's really close to the max number of arguments and would require a massive overhaul of the application.
    models.py:9:0: R0903: Too few public methods (1/2) (too-few-public-methods) : Unnecessary to add more methods
    models.py:5:0: W0611: Unused import flask_sqlalchemy (unused-import) : Import is actually nesscary to prevent werid behavior, pylint just does not know this.

### apifunctions.py
    apifunctions.py:48:0: R0914: Too many local variables (26/15) (too-many-locals) : Extremely hard to remove this many variables
    apifunctions.py:134:16: W0631: Using possibly undefined loop variable 'property' : It is defined
    apifunctions.py:153:4: W0612: Unused variable 'out_of_bound' (unused-variable) : Not needed.
    apifunctions.py:48:0: R0912: Too many branches (13/12) (too-many-branches) : One extra branch
    apifunctions.py:157:0: R0914: Too many local variables (25/15) (too-many-locals) : Duplicate error
    apifunctions.py:251:4: W0612: Unused variable 'out_of_bound' (unused-variable) : Duplicate error

### email_file.py
    No linting warnings or errors.
    
### rental_listings_api
    rental_listings_api.py:36:0: R0914: Too many local variables (22/15) (too-many-locals) : Extremely hard to remove this many variables
    rental_listings_api.py:67:8: R1705: Unnecessary "else" after "return" (no-else-return) : This error should not show up.
    rental_listings_api.py:121:4: W0612: Unused variable 'out_of_bound' (unused-variable) : Not needed.
    
### walkscore_api.py
    walkscore_api.py:54:4: W0612: Unused variable 'out_of_bound' (unused-variable) : Not needed.

## FacebookButton.jsx
  3:8  error  'ReactDOM' is defined but never used  no-unused-vars

## SearchEngine.jsx
  63:7   warning  Unexpected alert                             no-alert
  79:7   warning  Unexpected alert                             no-alert
  81:11  error    'changeLoad' is missing in props validation  react/prop-types

## SearchHistory.jsx
  6:40  error  A constructor name should not start with a lowercase letter  new-cap
  7:48  error  A constructor name should not start with a lowercase letter  new-cap

## SearchListings.jsx
   23:1   error  This line has a length of 109. Maximum allowed is 100  max-len
   26:1   error  This line has a length of 119. Maximum allowed is 100  max-len
  104:11  error  'changeLoad' is missing in props validation            react/prop-types

## Socket.jsx
  3:1  error  Prefer default export  import/prefer-default-export

## In Terminal
1. Must run this if psql is not running: sudo service postgresql start
2. Than must source API keys.
3. Run python app.py

# Individual Contributions

Neha Jagtap:
 - Created backend code for function to call Walkscore API and return data about Walkscore, travel times, etc. 
 - Added frontend display to show information from Walkscore
 - Created backend code for function to call Realtor API to include rental listings in addition to houses on sale
 - Added option for user on UI to choose between searching for rental listings and home listings
 - Added feature for user to sort display of listings by price (either low to high or high to low)
 - Added type checking for user input on frontend and backend of code; if user enters incorrect information, an alert will display to inform them
 - Initialized integration of CircleCI into the project
 - Styled the landing page using Material UI and CSS
 - Added written content to landing page (About, Steps, Creation of Our App, Links, Made By)
 - Styled the search page with the search input and search listings
 - Added a navbar to the top of the search page which has an icon for the user to click on that leads them to the Search History page or to the landing page; home button on the navbar allows the user to scroll to the top of the page 
 - Styled the search history page with Material UI
 - Reformatted code so that functions that called the Google Maps API were in a new file
 - Linted Javascript files with ESLint
 - Was PM for Week 5

Kevin Ng:
 - Implemented Facebook OAuth
 - Wrote Unit Testing for app.py, apifunctions.py, models.py, rental_listings_api.py, walkscore_api.py
 - Deployed to Heroku
 - Troubleshooted CircleCI and successfully built and deployed to Heroku
 - Created the loading animation for our contents page
 - Created feature for user to click a previous search and redirect user to contents page with the new search
 - Create a frontend response to no listings being returned
 - PM for week 3

Matthew Meeh
 - Redid models.py to reduce unnesscary code and redefined what we stored.
 - Linted all the testing files for the first and last time.
  -Linted all the files again (includes both pylinting and eslinting).
 - Tested database side manually again.
 - I built the frontend to search history.
  -I created a new file email_file.py to create an email class to fix the linting error for the global variable email.
 - Fixed bugs with the some of the testing files, when they broke on my branches (not including the merging branches). 
 
 Ali Alkhateeb
 - Wrote functions to calculate the commute times between every listing.
 - Implemented the functionality to display dynamic google maps for each listing.
 - Wrote code to convert a google place id  to an appropriate iframe link.
 - formatted api code and linted files using pylint/eslint.
 - General Troubleshooting.
 - PM for week 4.
