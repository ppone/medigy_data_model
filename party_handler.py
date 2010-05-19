#!/usr/bin/env python


# App Engine Imports
import logging
import os
import datetime
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from django.utils import simplejson
from google.appengine.api.labs import taskqueue

# Data Model Imports
import party_model


# Helper Imports
import helpers,notification

class PartyHandler(webapp.RequestHandler):
  
  # Retrieve a list of all the Users.
  def get(self):
    if  len(self.request.params) == 0:
      users_json = helpers.build_list_json(User.all())
      # Set the response content type and dump the json
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(simplejson.dumps(users_json))
    else:
      users_json = []
      if len(self.request.params) == 2:
        user = self.request.params['loginName']
        password = self.request.params['password']
        q = db.GqlQuery("SELECT * FROM User WHERE loginName = %s" % user)
        result = q.fetch(2)
        if len(result) == 0:
          users_json = []
        else:
          # This is really crappy, it works for now, but I'm not proud of it...
          if len(password.strip().replace("\'","")) == 0 or password == None:
            password = "'None'"
          if "'%s'" % result[0].password == password or (len(result[0].password) == 0 and password == "'None'"):
            result[0].authToken = helpers.generateAuthToken()
            result[0].put()
            users_json = helpers.build_list_json(User.all())
          else:
            users_json = []
      else:
        users_json = []
      # Set the response content type and dump the json
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(simplejson.dumps(users_json))
  
  # Create a new User
  def post(self):
    if len(self.request.params) > 0:
      if helpers.authorized(self.request.params['UUID'], self.request.params['ATO'], self.request.params['action']):
        # collect the data from the record
        user_json = simplejson.loads(self.request.body)
        
        # create a user
        user = helpers.apply_json_to_model_instance(User(), user_json)
        # save the new user
        user.put()
        
        guid = user.key().id_or_name()
        new_url = "/tasks-server/user/%s" % guid
        user_json["id"] = guid
        
        self.response.set_status(201, "User created")
        self.response.headers['Location'] = new_url
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(simplejson.dumps(user_json))
      else:
        self.response.set_status(401, "Not Authorized")
    else:
      user_json = simplejson.loads(self.request.body)
      user = helpers.apply_json_to_model_instance(User(), user_json)
      user.authToken = helpers.generateAuthToken()
      user.put()
      guid = user.key().id_or_name()
      new_url = "/tasks-server/user/%s" % guid
      user_json["id"] = guid
      self.response.set_status(201, "User created")
      self.response.headers['Location'] = new_url
      self.response.headers['Content-Type'] = 'text/json'
      self.response.out.write(simplejson.dumps(user_json))


class UserHandler(webapp.RequestHandler):
  # retrieve the user with a given id
  def get(self, guid):
    # find the matching user
    key = db.Key.from_path('User', int(guid))
    user = db.get(key)
    if not user == None:
      guid = "%s" % user.key().id_or_name()
      
      user_json = { "id": "%s" % guid,
        "name": user.name,
        "loginName": user.loginName, "role": user.role,
        "preferences": user.preferences if user.preferences != None else {},
        "authToken": user.authToken if user.authToken != None else '',
        "email": user.email if user.email != '' else '',
        "createdAt": user.createdAt if user.createdAt != None else 0,
        "updatedAt": user.updatedAt if user.updatedAt != None else 0 }
      
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(simplejson.dumps(user_json))
    
    else:
      self.response.set_status(408, "User not found [%s]" % guid)
  
  # Update an existing record
  def put(self, guid):
    # find the matching user
    key = db.Key.from_path('User', int(guid))
    user = db.get(key)
    if not user == None:
      
      # collect the data from the record
      user_json = simplejson.loads(self.request.body)
      # The following keeps Guests and Developers and Testers from being able
      # to change their role.
      currentUserId = self.request.params['UUID']
      cukey = db.Key.from_path('User', int(currentUserId))
      cuser = db.get(cukey)
      if str(user.role) != user_json['role'] and str(cuser.role) != "_Manager":
        user_json['role'] = str(user.role)
        self.response.set_status(401, "Not Authorized")
      # update the record
      user = helpers.apply_json_to_model_instance(user, user_json)
      # save the record
      user.put()
      # return the same record...
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(simplejson.dumps(user_json))
    else:
      self.response.set_status(404, "User not found")
  
  # delete the user with a given id
  def delete(self, guid):
    if helpers.authorized(self.request.params['UUID'], self.request.params['ATO'], self.request.params['action']):
      # find the matching user and delete it if found
      key = db.Key.from_path('User', int(guid))
      user = db.get(key)
      if not user == None:
        user.delete()
        self.response.set_status(204, "Deleted")
      else:
        self.response.set_status(404, "Not Found")
    else:
      self.response.set_status(401, "Not Authorized")



def main():
  application = webapp.WSGIApplication([(r'/tasks-server/user?$', UsersHandler),
    (r'/tasks-server/project?$', ProjectsHandler),
    (r'/tasks-server/task?$', TasksHandler),
    (r'/tasks-server/watch?$', WatchesHandler),
    (r'/tasks-server/user/([^\.]+)?$', UserHandler),
    (r'/tasks-server/project/([^\.]+)?$', ProjectHandler),
    (r'/tasks-server/task/([^\.]+)?$', TaskHandler),
    (r'/tasks-server/watch/([^\.]+)?$', WatchHandler),
    (r'/mailer', MailWorker)],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()