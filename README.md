[![Build Status](https://travis-ci.org/fgkinus/ride-my-way.svg?branch=master)](https://travis-ci.org/fgkinus/ride-my-way)
[![Coverage Status](https://coveralls.io/repos/github/fgkinus/ride-my-way/badge.svg?branch=master)](https://coveralls.io/github/fgkinus/ride-my-way?branch=master)

Welcome to to Ride-my-Way, a Ride sharing app for all.

 The project is meant to be a ride sharing/ car pooling platform where drivers 
 can add ride offers, the ride offers are viewed by passengers, the passengers may the make a request to join 
 the ride. The driver has the choice to approve or reject a ride.

Created using FLask , it implements a Flask Rest Plus API restful API endpoints.Th
project employs Flask-JWT-Extended as the authentication backend.
 The backend further uses a Postgres DB to persistently store data. The project however does not use an 
 ORM and the backend queries the database directly. 
 
 Unit testing is carried out using pytest and all tests reside within the project.

Among the features to come include an ability for passengers to share rides with their friends
and real time notifications for rides.
The current build is currently hosted on heroku at 
https://ride-my-way-v1.herokuapp.com/