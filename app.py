# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
#import sqlite3


# create the application object
app = Flask(__name__)

# config
import os
app.config.from_object(os.environ['APP_SETTINGS'])
#print os.environ['APP_SETTINGS']

#create the sqlalchemy object
db = SQLAlchemy(app)
from models import *

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
	groceries = db.session.query(BlogPost).all()
	grocdata = []
	for groc in groceries:
		grocdata.append(dict(item=groc.title.encode("utf-8"),description=groc.description.encode("utf-8"), timeadded=groc.time.encode("utf-8")))
	print grocdata
	print("length of grocdata is: ",len(grocdata))
	return render_template('index.html', groceries=grocdata)  # render a template
    


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

# don't need this because we are using sqlalchemy:
# def connect_db():
# 	return sqlite3.connect(app.databse)
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)