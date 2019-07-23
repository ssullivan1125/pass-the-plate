import jinja2
import os
import webapp2

the_jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Welcome to Pass the Plate")

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        hogwarts_houses = House.query().order(House.name).fetch()
        start_template = jinja_env.get_template("templates/houselist.html")
        self.response.write(start_template.render({'house_info' : hogwarts_houses}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', HouseHandler),
    ('/homepage', LoadDataHandler)
], debug=True)
