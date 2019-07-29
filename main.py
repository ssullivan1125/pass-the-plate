import webapp2
import os
import jinja2
import random
from google.appengine.ext import ndb
from google.appengine.api import users
from models import PtpUser
from models import SavePost


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/homepage.html')
        self.response.write(template.render())

class ViewPostHandler(webapp2.RequestHandler):
    def get(self):

        view_all_posts = SavePost.query().fetch()

        template_vars = {
            "view_all_posts": view_all_posts
        }

        template = jinja_env.get_template('templates/foodlistings.html')
        # print('Hi! Here are the food listings!')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(template_vars))


    def post(self):
        view_all_posts = SavePost.query().fetch()

        organization_input = self.request.get('organization')
        produce_input = self.request.get('produce')
        expiration_input = self.request.get('expiration')
        location_input = self.request.get('location')
        delivery_input = self.request.get('delivery')

        new_post = SavePost( organization=organization_input, produce=produce_input, expiration=expiration_input, location=location_input, delivery=delivery_input)
        new_post.put()

        view_all_posts.insert(0, new_post)

        template_vars = {
            "new_post": new_post,
            "view_all_posts": view_all_posts
        }

        print(view_all_posts)
        print(new_post)

        template = jinja_env.get_template('templates/foodlistings.html')
        self.response.write(template.render(template_vars))

class LookAtPostHandler(webapp2.RequestHandler):
    def get(self):
        keystr = self.request.get("postkey")

        post = ndb.Key(urlsafe=keystr).get()

        template_vars = {
            "post": post
        }

        template = jinja_env.get_template('templates/listinginfo.html')
        # print('Hi! Here are the food listings!')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(template_vars))


class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
      email_address = user.nickname()
      ptp_user = PtpUser.query().filter(PtpUser.email == email_address).get()

      if ptp_user:
          self.response.write(
          "Looks like you're registered. Thanks for using our site!")
      else:
          self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/account">
            <input type="text" name="first_name" placeholder = "First Name">
            <input type="text" name="last_name" placeholder = "Last Name">
            <input type="text" name="organization_name" placeholder = "Organization Name">
            <input type="text" name="organization_type" placeholder = "Distributor or Reciever">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))
    else:
      login_url = users.create_login_url('/')
      template_vars = {
      "login_url": login_url
      }
      template = jinja_env.get_template('templates/SignupPage.html')
      self.response.write(template.render(template_vars))

  def post(self):
     user = users.get_current_user()
     ptp_user = PtpUser(
         first_name=self.request.get('first_name'),
         last_name=self.request.get('last_name'),
         organization_name=self.request.get('organization_name'),
         organization_type=self.request.get('organization_type'),
         email=user.nickname())

     ptp_user.put()
     self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
         ptp_user.organization_name)

class CreatePostHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_env.get_template("templates/newpost.html")
        self.response.write(start_template.render())

    def post(self):
        organization_var = self.request.get('organization')
        produce_var = self.request.get('produce')
        expiration_var = self.request.get('expiration')
        location_var = self.request.get('location')
        delivery_var = self.request.get('delivery')

        the_post_var = {
            "organization_var": organization_var,
            "produce_var": produce_var,
            "expiration_var": expiration_var,
            "location_var": location_var,
            "delivery_var": delivery_var
        }
        template = jinja_env.get_template('/foodlistings.html')
        self.response.write(template.render(the_post_var))

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_env.get_template("templates/aboutus.html")
        self.response.write(start_template.render())


app = webapp2.WSGIApplication([
  ('/', WelcomeHandler),
  ('/account', MainHandler),
  ('/newpost', CreatePostHandler),
  ('/listings', ViewPostHandler),
  ('/listinginfo', LookAtPostHandler),
  ('/about', AboutHandler)


], debug=True)



# class CreatePostHandler(webapp2.RequestHandler):
#      def get(self):
#         template = jinja_env.get_template('templates/homepage.html')
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.write(create_template.render())
#
#      def post(self):
#         curr_message_txt = self.request.get('message')
#         curr_user = user.get_current_user()
#         intended_reciever = 'test@gmail.com'
#
#         possible_reciever = PtpUser.query(intended_reciever == PtpUser.email).get()
#
#         curr_message = Message(
#         message_txt = curr_message_txt,
#         sender = curr_user,
#         reciever = intended_reciever
#         )
#
#         message_key = curr_message.put()
#
#         sending_user = PtpUser.query(curr_user.nickname == PtpUser.email.get())
#
#         sending_user.messages.append(message_key).put()
#
#         self.redirect('/profile')
