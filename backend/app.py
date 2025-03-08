from flask import Flask, request, render_template ,jsonify
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL'))
db = client['flask-app']
users = db['users']

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email or not password:
       return 'Please fill all fields'
    if users.find_one({'email': email}):
       return jsonify({'message': 'User already exists'}), 400
    try:
       users.insert_one({
           'name': name,
           'email': email,
           'password': password
       })
       return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
       return jsonify({'message': 'An error occurred'}), 500
   
@app.route('/login', methods=['POST'])
def login():
   email = request.form.get('email')
   password = request.form.get('password')
   if not email or not password:
       return 'Please fill all fields'
   user = users.find_one({'email': email, 'password': password})
   if not user:
       return jsonify({'message': 'Invalid credentials'}), 400
   return jsonify({'message': 'Login successful'}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users_list = users.find()
    users_list = list(users_list)
    for user in users_list:
        user['_id'] = str(user['_id'])
    return jsonify(users_list)



if __name__ == '__main__':
   app.run(host='0.0.0.0', port='3000',debug=True)