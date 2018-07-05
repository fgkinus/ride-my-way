[![Build Status](https://travis-ci.org/fgkinus/ride-my-way.svg?branch=master)](https://travis-ci.org/fgkinus/ride-my-way)
[![Coverage Status](https://coveralls.io/repos/github/fgkinus/ride-my-way/badge.svg?branch=master)](https://coveralls.io/github/fgkinus/ride-my-way?branch=master)

Welcome to to Ride-my-Way, a Ride sharing app for all.

## instructions
To get all dependencies run : *pip install -t requirements.txt* 
## flask configuration 
To configure flask please make sure that a *.env* file exists in the root folder. 
Add the following configuration settings are:


``export FLASK_APP="app.py"``

``export SECRET="your secret key goes here"``

``export APP_SETTINGS="development"``

**NB** App settings  is configured to *development* by default. to modify this behavior
see other contexts in *config.py* file and their presets
## database environment setup

The project depends on Postgres database and as such you will need to have it on your local machine. Thw default user 
is *postgres* with no password. The application initialises a database with the name as indicated
in the *.env* and creates all the required tables.if the table already exists
then it assumes the required table ar present. Please make sure if its the first setup that you avoid
using a name to a database that already exists 

To change this modify the environment fie as follows:
`` 
export DB_USER = 'your user name' 
export DB_NAME = 'your database name'
export DB_PASSWORD = 'your database password'
``

__NB__ :please note that the db user must have access to the **postgres** database since this database
is used to establish the initial connection. 

## Testing
tests are configured to run using pytest. Run the tests using the following script:

``python -m pytest``

due to the external *.env* follow this guide to import environment variables before tests can run:
https://github.com/quiqua/pytest-dotenv

## demo
