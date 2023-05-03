#!/bin/bash

rm db.sqlite3
rm -rf ./roamapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations roamapi
python3 manage.py migrate roamapi
python3 manage.py loaddata users
python3 manage.py loaddata token
python3 manage.py loaddata traveler
python3 manage.py loaddata trip
python3 manage.py loaddata tag
python3 manage.py loaddata category
python3 manage.py loaddata item
# python3 manage.py loaddata state
python3 manage.py loaddata destinationstatus
python3 manage.py loaddata destination
python3 manage.py loaddata triptag
python3 manage.py loaddata tripdestination