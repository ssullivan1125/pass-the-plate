from google.appengine.ext import ndb

class PtpUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  organization_name = ndb.StringProperty()
  organization_type = ndb.StringProperty()
  email = ndb.StringProperty()
  messages = ndb.KeyProperty(repeated = True)

class Message(ndb.Model):
    message_txt = ndb.TextProperty()
    sender = ndb.KeyProperty()
    reciever = ndb.KeyProperty()

class SavePost(ndb.Model):
    organization = ndb.StringProperty()
    produce = ndb.StringProperty()
    expiration = ndb.StringProperty()
    location = ndb.StringProperty()
    delivery = ndb.StringProperty()


#  class Post(ndb.Model):
#      title_id = ndb.StringProperty(required = True)
#      content_id = ndb.StringProperty(required = True)
#
# class Organization(ndb.Model):
#     posts = ndb.KeyProperty(Post, repeated = True)
