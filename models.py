from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class GroceryItem(db.Model):

    __tablename__ = "groceries"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    time = db.Column(db.String,nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, title, description, time):
        self.title = title
        self.description = description
        self.time = time

    def __repr__(self):
        return "{}-{}-{}".format(self.title, self.description, self.time)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = relationship("GroceryItem", backref="author")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return 'name {}'.format(self.name)
