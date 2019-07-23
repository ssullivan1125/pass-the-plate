import jinja2
import os
import webapp2

the_jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
