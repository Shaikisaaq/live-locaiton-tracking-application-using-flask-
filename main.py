from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import bcrypt


app=Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client['hackathon']
users_collection = db['users']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user into database
        users_collection.insert_one({'username': username, 'password': hashed_password})

        return redirect(url_for('login'))

    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Find user in database
        user = users_collection.find_one({'username': username})

        if user:
            # Check password
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                # Authentication successful, redirect to dashboard or home page
                print('true that the password has matched')
                return redirect(url_for('hello'))
            else:
                # Incorrect password
                error_message = 'Incorrect password'
        else:
            # User not found
            error_message = 'User not found'

    return render_template('login.html', error_message=error_message)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/hello")
def hello():
    return render_template('hello.html')

if __name__ == '__main__':
    app.run(debug=True) 