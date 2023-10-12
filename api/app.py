from flask import Flask, request, jsonify, redirect, g
from flask_cors import CORS
from pymongo import MongoClient
import jwt
import datetime
import functools
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devops_in_a_nutshell'
CORS(app, origins="*")

# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client['movie_database']
movies_collection = db['movies']
short_urls_collection = db['short_urls']

# Simulated user database
users = {
    'admin': {'password': 'qwerty', 'role': 'admin'},
    'user1': {'password': 'qwerty', 'role': 'user'},
    'user2': {'password': 'qwerty', 'role': 'user'}
}

# Custom wrapper to check user role
def role_check(allowed_roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token or not token.startswith('Bearer '):
                return jsonify({'error': 'Bearer token missing'}), 401
            token = token.split('Bearer ')[1]

            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                g.user = payload
                role = payload['role']
                if role in allowed_roles:
                    return func(*args, **kwargs)
                else:
                    return jsonify({'error': 'Forbidden'}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
        return wrapper
    return decorator

# Login route to get JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    if user and user['password'] == password:
        token_body = {
            'username': username,
            'role': users[username]['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(token_body, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

def timestamp_to_base62(timestamp):
    base62_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    base62_string = ""

    while timestamp > 0:
        remainder = timestamp % 62
        base62_string = base62_chars[remainder] + base62_string
        timestamp //= 62

    return base62_string

# Create a new short URL
@app.route('/shorturl', methods=['POST'])
@role_check(allowed_roles=['admin', 'user'])
def create_short_url():
    data = request.json
    long_url = data.get('long_url')
    username = g.user.get('username')

    timestamp_ms = int(time.time() * 1000)
    short_url = timestamp_to_base62(timestamp_ms)

    short_urls_document = {
        '_id': short_url,
        'long_url': long_url,
        'user': username
    }
    short_urls_collection.insert_one(short_urls_document)

    return jsonify({'message': 'Short URL created', 'short_url': short_url}), 201

@app.route('/shorturl/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):
    short_url_document = short_urls_collection.find_one({'_id': short_url})
    if short_url_document:
        long_url = short_url_document['long_url']
        return redirect(long_url, code=302)
    return jsonify({'error': 'Short URL not found'}), 404

# Get all short URLs
@app.route('/shorturl', methods=['GET'])
@role_check(allowed_roles=['admin', 'user'])
def get_short_urls():
    username = g.user.get('username')
    short_urls = list(short_urls_collection.find({'user': username}))
    return jsonify(short_urls)

# Delete a short URL
@app.route('/shorturl/<short_url>', methods=['DELETE'])
@role_check(allowed_roles=['admin', 'user'])
def delete_short_url(short_url):
    username = g.user.get('username')
    if short_urls_collection.find_one({'_id': short_url, 'user': username}):
        short_urls_collection.delete_one({'_id': short_url, 'user': username})
        return jsonify({'message': 'Short URL deleted'})
    return jsonify({'error': 'Short URL not found'}), 404

