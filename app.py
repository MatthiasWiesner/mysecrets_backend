import os
import json
import hashlib
from flask import Flask, request, Response
from functools import wraps
from flask_orator import Orator
from flask import make_response
from flask import jsonify
from flask_cors import CORS

from orator.orm import belongs_to
from orator.orm import has_many

from pprint import pprint

config = {
    "development": "config.DevelopmentConfig",
    "production": "config.ProductionConfig"
}

app = Flask(__name__)

app = Flask(__name__)
CORS(app)

environment = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[environment])

db = Orator(app)


class User(db.Model):
    __fillable__ = ['name', 'password']

    def __repr__(self):
        return '<User %r>' % self.name


class Secret(db.Model):
    __fillable__ = ['data']

    def __repr__(self):
        return '<Secret %r>' % self.name


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    user = User.where('name', '=', username).first()
    if user:
        return hashlib.sha256(password).hexdigest() == user.password
    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    resp = jsonify(success=True)
    return resp


@app.route('/mysecrets', methods=['GET'], strict_slashes=False)
@requires_auth
def get_mysecrets():
    secrets = Secret.all()
    return json_response(secrets.to_json())


@app.route('/mysecrets/<secret_id>', methods=['GET'])
def get_mysecrets_by_id(secret_id):
    secret = Secret.find(secret_id)
    return json_response(secret.to_json())


@app.route('/mysecrets', methods=['POST'])
def post_mysecret():
    secret = Secret()
    secret.data = request.form['data']
    secret.save()

    resp = jsonify(success=True)
    return resp


@app.route('/mysecrets/<secret_id>', methods=['PUT'])
def put_mysecret(secret_id):
    secret = Secret.find(secret_id)
    secret.data = request.form['data']
    secret.save()

    resp = jsonify(success=True)
    return resp


@app.route('/mysecrets/<secret_id>', methods=['DELETE'])
def delete_mysecret(secret_id):
    Secret.find(secret_id).delete()
    resp = jsonify(success=True)
    return resp


def json_response(json_data):
    r = make_response(json_data)
    r.mimetype = 'application/json'
    return r
