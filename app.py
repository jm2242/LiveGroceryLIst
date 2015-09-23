# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, g, jsonify
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
#import sqlite3


# create the application object
app = Flask(__name__)

# config
import os
import json
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
	groceries = db.session.query(GroceryItem).all()
	grocdata = []
	for groc in groceries:
		grocdata.append(dict(item=groc.title.encode("utf-8"),description=groc.description.encode("utf-8"), timeadded=groc.time.encode("utf-8")))
	#print grocdata
	#print("length of grocdata is: ",len(grocdata))
	return render_template('index.html', groceries=grocdata)  # render a template
   
#save user added data, eventually also add data that user deleted here   
@app.route('/save')
def save():
	# get the list of new items
	savedItems = json.loads(request.args.get('added'))
	deletedItems = json.loads(request.args.get('deleted'))
	print("The saved items are : ",savedItems)
	print("The deleted items are: ", deletedItems)
	#if savedItems contains items, then store in database
	if savedItems:
		for item in savedItems:
			#if the item is in the deleted list also, no need to add
			if item not in deletedItems:
				db.session.add(GroceryItem(item[0],item[1],item[2]))
				db.session.commit()
			else:
				print("the item is also queued to be deleted, so don't add it")
	# if deletedItems contains items, then delete the items 
	if deletedItems:
		for item in deletedItems:

			#if the item was not added during the current session
			if item not in savedItems:
				grocery_item = item['id'].encode("utf-8")
				timeadded = item['timeadded'].encode("utf-8")
				description = item['description'].encode("utf-8")
				item_to_be_deleted_as_grocery_object = db.session.query(GroceryItem).\
				filter(GroceryItem.title == grocery_item, GroceryItem.description == description, GroceryItem.time == timeadded).one()
				#print item_to_be_deleted_as_grocery_object
				db.session.delete(item_to_be_deleted_as_grocery_object)
				db.session.commit()
			else:
				print("the item to be deleted was only added on client side, never commited to database")
	return jsonify(result="flask received the array of data")
	


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




