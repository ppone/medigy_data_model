""" This File holds the model definitions used in this app.
  Author: Parag Patel
  Date: 09-30-2009
  Last Modified: 12-08-2009
"""

from google.appengine.ext import db

class Insurance(db.Model):
    type = db.StringProperty()
    insurance_company = db.StringProperty()
    company_address = db.StringProperty()
    name_of_insured = db.StringProperty()
    relation_to_patient = db.StringProperty()
    group_number = db.StringProperty()
    effective_date = db.DateProperty()
    benefit_code = db.StringProperty()
    id = db.StringProperty()
    medicare_id = db.StringProperty()
    medicaid_id = db.StringProperty()
    perscription_drug_plan  = db.StringProperty()
    other_coverages = db.StringProperty()


