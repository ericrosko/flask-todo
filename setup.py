#!/usr/bin/env python3

"""
Scripts to run to set up our database

IMPORTANT: In addition to running this once to set things up, you
must also assing this environmental variable in the terminal:
export SECRET_KEY=efkje323kjfdf
The key can be any number you want.
See all env variables by typing 'env' in the terminal.
This key is used here:
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()
It is used to encode the web session.
"""

from datetime import datetime
from model import db, User, Task
from passlib.hash import pbkdf2_sha256

# Create the database tables for our model
db.connect()
db.drop_tables([User, Task])
db.create_tables([User, Task])

bob = User(name='bob', password=pbkdf2_sha256.hash("b"))
bob.save() # don't forget to save!!!

user = User(name='admin', password=pbkdf2_sha256.hash("a"))
user.save() # don't forget to save!!!

user = User(name='a', password=pbkdf2_sha256.hash("a"))
user.save() # don't forget to save!!!

Task(name="Do the laundry.").save()
Task(name="Do the dishes.", performed=datetime.now(), performed_by=bob).save()

if __name__ == "__main__":
    pass
