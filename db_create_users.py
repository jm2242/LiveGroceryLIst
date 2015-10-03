__author__ = 'jonathanmares'
from project import db
from project.models import User

#insert data
db.session.add(User("Jonathan", "jmares93@gmail.com","pascode"))
db.session.add(User("admin","ad@min.com","admin"))

db.session.commit()