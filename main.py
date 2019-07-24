import webapp2
import os
import jinja2
import random
from google.appengine.api import users
from google.appengine.ext import ndb

class PtpUser(ndb.Model):
  organization_name = ndb.StringProperty()
  email = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      logout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
      email_address = user.nickname()
      ptp_user = PtpUser.query().filter(PtpUser.email == email_address).get()

      if ptp_user:
          self.response.write(
          "Looks like you're registered. Thanks for using our site!")
      else:
          self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            <input type="text" name="organization_name">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, logout_link_html))
    else:
      login_url = users.create_login_url('/')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      self.response.write('Please log in.<b>' + login_html_element)

  def post(self):
     user = users.get_current_user()
     ptp_user = PtpUser(
         organization_name=self.request.get('organization_name'),
         email=user.nickname())
     ptp_user.put()
     self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
         ptp_user.organization_name)

app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)
