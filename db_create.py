from app import db
from models import BlogPost

#create the database and the db tables
#initializes based on schema defined in models.py
db.create_all()

#insert
db.session.add(BlogPost("Good","I\'m good."))
db.session.add(BlogPost("Food","Wonderful"))
db.session.add(BlogPost("postgres","we're setting up a local postgres instance"))

#commit 
db.session.commit()