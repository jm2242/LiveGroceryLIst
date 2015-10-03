# import the Flask class from the flask module
from project import app, db
from project.models import GroceryItem
from flask import render_template, redirect, url_for, request, session, flash, g, jsonify, Blueprint
from functools import wraps
from sqlalchemy.orm.exc import NoResultFound
import json



# config #
home_blueprint = Blueprint('home', __name__,template_folder='templates')


# helper functions ###

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash('You need to login first.')
            return redirect(url_for('users.login'))

    return wrap

#### routes ######

# use decorators to link the function to a url
@home_blueprint.route('/')
@login_required
def home():
    groceries = db.session.query(GroceryItem).all()
    grocdata = []
    for groc in groceries:
        grocdata.append(dict(item=groc.title.encode("utf-8"), description=groc.description.encode("utf-8"),
                             timeadded=groc.time.encode("utf-8"), author=groc.author.name.encode("utf-8")))
    # print grocdata
    # print("length of grocdata is: ",len(grocdata))
    return render_template('index.html', groceries=grocdata)  # render a template


# save user added data, eventually also add data that user deleted here
@home_blueprint.route('/save')
def save():
    # get the list of new items
    savedItems = json.loads(request.args.get('added'))
    deletedItems = json.loads(request.args.get('deleted'))
    print("The saved items are : ", savedItems)
    print("The deleted items are: ", deletedItems)
    # if savedItems contains items, then store in database
    if savedItems:
        for item in savedItems:
            # if the item is in the deleted list also, no need to add
            if item not in deletedItems:
                db.session.add(GroceryItem(item[0], item[1], item[2], item[3]))
                db.session.commit()
            else:
                print("the item is also queued to be deleted, so don't add it")
    # if deletedItems contains items, then delete the items
    if deletedItems:
        for item in deletedItems:

            # if the item was not added during the current session
            if item not in savedItems:
                grocery_item = item['id'].encode("utf-8")
                timeadded = item['timeadded'].encode("utf-8")
                description = item['description'].encode("utf-8")
                try:
                    item_to_be_deleted_as_grocery_object = db.session.query(GroceryItem). \
                        filter(GroceryItem.title == grocery_item, GroceryItem.description == description,
                               GroceryItem.time == timeadded).one()
                    # print item_to_be_deleted_as_grocery_object
                    db.session.delete(item_to_be_deleted_as_grocery_object)
                    db.session.commit()
                except NoResultFound:
                	print("Oops, that row is not in the database")

            else:
                print("the item to be deleted was only added on client side, never commited to database")
    return jsonify(result="flask received the array of data")


@home_blueprint.route('/welcome')
def welcome():
    return render_template('home.welcome.html')  # render a template




