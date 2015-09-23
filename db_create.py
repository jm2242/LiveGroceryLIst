from app import db
from models import GroceryItem

# delete database contents
# GroceryItem.query.delete()

#create the database and the db tables
#initializes based on schema defined in models.py
db.create_all()

#insert these only for testing/placeholding
# db.session.add(GroceryItem('Cookies','I am good.','11:10AM'))
# db.session.add(GroceryItem('Food','Wonderful','14:12:34, Tue, Sep 22'))
# print db.session.query(GroceryItem).all()

#commit 
db.session.commit()
