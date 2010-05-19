""" This File holds the model definitions used in this app.
  Author: Parag Patel
  Date: 09-30-2009
  Last Modified: 12-08-2009
"""

from google.appengine.ext import db

class User(Party):
  """ This is the User Model"""
  name = db.StringProperty(required=True, default="_FirstLast")
  loginName = db.StringProperty(required=True, default="_Initials")
  role = db.StringProperty(required=True, default="_FrontOffice")
  #preferences = db.StringProperty() -- NOT Used yet.
  email = db.StringProperty(required=False)
  password = db.StringProperty(required=False)
  authToken = db.StringProperty(required=False)
  createdAt = db.IntegerProperty(required=False)
  updatedAt = db.IntegerProperty(required=False)


