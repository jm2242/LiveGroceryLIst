from app import db

class GroceryItem(db.Model):

	__tablename__ = "groceries"

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	time = db.Column(db.String,nullable=False)

	def __init__(self, title, description,time):
		self.title = title
		self.description = description
		self.time = time

	def __repr__(self):
		return "{}-{}-{}".format(self.title, self.description, self.time)
