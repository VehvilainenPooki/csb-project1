# csb-project1
This is an university of Helsinki courses project: [https://cybersecuritybase.mooc.fi/](https://cybersecuritybase.mooc.fi/)

## environment
- python 3.11 (probably many other versions work also)
- django
- sqlite

## install
1. get python:
https://www.python.org/downloads/

2. get django:
https://docs.djangoproject.com/en/5.1/topics/install/#installing-official-release

3. clone the repo

4. setup the database with:
```
python manage.py migrate
```
## run
Server will launch with:
```
python manage.py runserver
```
The server url will be written in the console. Something like http://127.0.0.1:8000/.
