""" This File holds the model definitions used in this app.
  Author: Parag Patel 
  Date: 09-30-2009
  Last Modified: 12-08-2009
"""

from google.appengine.ext import db

class Contact(db.Model):
    contact_info = db.StringProperty(required=True)
    contact_type = db.StringProperty(required=True)