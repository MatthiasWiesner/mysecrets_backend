import os
import json
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
    __fillable__ = ['name']

    @belongs_to
    def category(self):
        return Category

    def __repr__(self):
        return '<Secret %r>' % self.name


class Category(db.Model):
    __fillable__ = ['name']

    @has_many
    def secrets(self):
        return Secret

    def __repr__(self):
        return '<Category %r>' % self.name


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    user = User.where('name', '=', username).first()
    if user:
        return password == user.password
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
    u = User.where('name', '=', 'matthias.wiesner').first()
    return json_response(u.to_json())


@app.route('/categories', methods=['GET'])
@requires_auth
def get_categories():
    categories = Category.all()
    return json_response(categories.to_json())


@app.route('/mysecrets', methods=['GET'])
@requires_auth
def get_mysecrets():
    secrets = Secret.order_by('name').get()
    for s in secrets:
        s.category
    return json_response(secrets.to_json())


@app.route('/mysecrets/path/<path>', methods=['GET'])
def get_mysecrets_by_path(path):
    pass


@app.route('/mysecrets/id/<secret_id>', methods=['GET'])
def get_mysecrets_by_id(secret_id):
    secret = Secret.find(secret_id)
    return json_response(secret.to_json())


@app.route('/mysecrets', methods=['POST'])
def post_mysecret():
    if 'id' in request.form:
        secret = Secret.find(request.form['id'])
    else:
        secret = Secret()

    secret.category_id = request.form['category_id']
    if 'category_txt' in request.form and request.form['category_txt']:
        # neue kategorie anlegen
        category = Category()
        category.name = request.form['category_txt']
        category.save()
        secret.category_id = category.id

    secret.name = request.form['name']
    secret.url = request.form['url']
    secret.credentials = request.form['credentials']
    try:
        tags = json.loads(request.form['tags'])
    except:
        tags = json.loads('[]')

    secret.tags = json.dumps(tags)
    secret.save()

    resp = jsonify(success=True)
    return resp


@app.route('/mysecrets/id/<secret_id>', methods=['DELETE'])
def delete_mysecret(secret_id):
    Secret.find(secret_id).delete()

    resp = jsonify(success=True)
    return resp


def json_response(json_data):
    r = make_response(json_data)
    r.mimetype = 'application/json'
    return r