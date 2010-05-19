""" This File holds the model definitions used in this app.
  Author: Parag Patel
  Date: 09-30-2009
  Last Modified: 12-08-2009
"""

from google.appengine.ext import db

class Facility(db.Model):
    description = db.StringProperty()
    work_phone = db.StringProperty()
    email = db.StringProperty()
    
