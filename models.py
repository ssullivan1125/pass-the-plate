from google.appengine.ext import ndb

class PtpUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  organization_name = ndb.StringProperty()
  organization_type = ndb.StringProperty()
  email = ndb.StringProperty()
