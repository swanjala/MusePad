# MusePad

![musejournal](https://user-images.githubusercontent.com/24252450/41875468-9e509112-78d3-11e8-894d-78a9f67f007b.png)


## About 
Muse-Pad is an Application Programming interface that let you write down your thoughts and special moments in your daily life.
Hosted on https://muse-pad.herokuapp.com

## Getting Started

Use the following steps to run the API on your localhost

## Set Prerequisites
intall the requirements for running the Application, preferably in a virtual environment running python3.x and activate it

```
pip install -r requirements.txt

```
### Installing

Set up the database

```
python manage.py db init

```

Migrate the data into the database by running 

```
python manage.py db migrate

```
Upgrade the database

```
python manage.py db upgrade

```

### Running Tests

In order to run the tests, type the folling in a terminal with an activated `bucketlist` virtual environment

```
python manage.py test

```
Ensure that you are in the same directory as manage.pygr

### Running The Application 

Start the server

```
python manage.py runserver

```

## Deployment
Add additional notes about how to deploy this on a lice system

## Built With 

* [FLASK](https://flask/pocoo.org) - The web framework used
* [NOSE](https://nose.readthedocs.io/en/latest/) - Testing framework
* [COVERALLS](https://coveralls.io/)- Used to generate RSS Feeds 

## Versioning

This is the first version on the Application Programming Interface 

## Author
* **Sam Wanajala** - [swanjala](https://github.com/swanjala)