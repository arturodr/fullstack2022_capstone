# QR tag Backend

This project constitutes the backend for the base of a system that helps identify objets or animals using QR codes. 
an application could be ID of pets using a QR code, the user can have one or more pets and associated info, the code is printed on the pet tag, when the QR is read the pet and user info are displayed.

## Getting Started

### Dependencies

#### Python 3.8+

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

It's recommended that a virtual enviroments is used.

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Initializing the database

We'll use manage.py to inicialize and migrate the database

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```


## Running the server

From within the root directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Endpoints documentation
```
Endpoints
GET '/users/'
GET '/users/{id}'
POST '/users/'
DELETE '/users/{id}'
GET '/tags/{id}'
POST '/tags/'
PATCH '/tags/{id}'
DELETE '/tags/{id}'
GET '/qr/{qr_id}'
```

## RBAC documentation

There are two profiles configured, a user and an admin. Also, the qr endpoint is publicly accessible.

- User
  - can `get:tags`
  - can `post:tags`
  - can `patch:tags`
  - can `delete:tags`
- Manager
  - can perform all actions