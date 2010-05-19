""" This File holds the model definitions used in this app.
  Author: Parag Patel
  Date: 09-30-2009
  Last Modified: 12-08-2009
"""

from google.appengine.ext import db

class Party(db.Model):
    name = db.StringProperty(required=True)
    contacts = db.ListProperty(db.Key)
    facilities = db.ListProperty(db.Key)
    qualifications = db.StringListProperty()
    type = db.StringProperty(required=True)