""" This File holds the model definitions used in this app.
  Author: Parag Patel
  Date: 09-30-2009
  Last Modified: 12-08-2009
"""

from google.appengine.ext import db

class Person(Party):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    middle_name = db.StringProperty()
    ssn = db.StringProperty()
    drivers_license = db.StringProperty()
    birth_date = db.DateTimeProperty(required=True)
    death_date = db.DateTimeProperty()
    marital_status = db.StringProperty(choices=set(['Single', 'Married', 'Divorced', 'Separated', 'Unknown']), default='Unknown')
    gender = db.StringProperty(choices=set(['Male', 'Female', 'Unknown']), default='Unknown')
    ethnicity = db.StringProperty(choices=set(['Caucasian', 'Hispanic', 'Asian', 'Native-American', 'African-American']))
    languages = db.StringListProperty()    #['English', 'Spanish', 'French', 'German', 'Chinese']
    user = db.ReferenceProperty(User)
    photo = db.ListProperty(db.Blob)
    type = db.StringProperty(choices=set(['Patient', 'Provider', 'Referring-Provider', 'Other']), default='Other')
    spouse_partner = db.SelfReferenceProperty()
    referred_by = db.StringProperty()
    parent = db.ListProperty(db.Key)
    ome_phone = db.StringProperty()
    cell_phone = db.StringProperty()
    work_phone = db.StringProperty()
    email = db.StringProperty()
    emergency_contact_name = db.StringProperty()
    emergency_contact_phone = db.StringProperty()
    emergency_contact_cell_phone = db.StringProperty()
    emergency_contact_work_phone = db.StringProperty()
    emergency_contact_address = db.StringProperty()
    emergency_contact_relation = db.StringProperty()
    doctor = db.ListProperty(db.Key)
    #personal medical history
    personalmedicalhistory=photo = db.Blob