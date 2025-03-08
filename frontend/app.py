from flask import Flask, render_template , request
import requests
from datetime import datetime

BACKEND_URL = 'http://localhost:3000'

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.today().strftime('%A')
    return render_template('index.html', day_of_week=day_of_week)

@app.route('/signup', methods=['POST'])
def signup():
    form_data = dict(request.form)
    response = requests.post(f'{BACKEND_URL}/signup', json=form_data)
    if response.status_code != 201:
        error_message = response.json().get('message')
        return render_template('index.html', error=error_message)
    return render_template('index.html', message='User created successfully')

@app.route('/get_users', methods=['GET'])
def get_users():
    response = requests.get(f'{BACKEND_URL}/users')
    users = response.json()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000',debug=True)