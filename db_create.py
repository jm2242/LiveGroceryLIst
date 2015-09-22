from app import db
from models import BlogPost

# delete database contents
BlogPost.query.delete()

#create the database and the db tables
#initializes based on schema defined in models.py
db.create_all()

#insert
db.session.add(BlogPost('Cookies','I am good.','11:10AM'))
db.session.add(BlogPost('Food','Wonderful','14:12:34, Tue, Sep 22'))
print db.session.query(BlogPost).all()

#commit 
db.session.commit()
