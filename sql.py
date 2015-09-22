import sqlite3
# creates databse
with sqlite3.connect("sample.db") as connection:
	#define cursor
	c = connection.cursor()
	# create new table
	c.execute("""DROP TABLE posts""")
	c.execute("""CREATE TABLE posts(title TEXT, description TEXT)""")
	c.execute('INSERT INTO posts VALUES("GOOD", "I\' m good.")')
	c.execute('INSERT INTO posts VALUES("Well", "I\' m well.")')

