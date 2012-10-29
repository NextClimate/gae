import os
from google.appengine.ext.webapp import template

import cgi
import datetime
import urllib
import wsgiref.handlers
import string

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp.util import run_wsgi_app

# this class holds a zip code and climate info. This is an
# entity in the datastore.

class Zipcode(db.Model):
  """Models an individual zipcode associated with climate change values"""
  zipcode=db.StringProperty()
  city = db.StringProperty(multiline=False)
  state = db.StringProperty(multiline=False)
  maxTobs_1990 = db.IntegerProperty()
  maxTa1_2050 = db.IntegerProperty()
  maxTa1_2090 = db.IntegerProperty()    
  maxTb2_2090 = db.IntegerProperty()

class UserNC(db.Model):
    """ This is a NextClimate user """
    name = db.StringProperty()
    FBid = db.StringProperty()
    gender = db.StringProperty()
    email = db.EmailProperty()
    birthday = db.DateProperty()
    firstName = db.StringProperty()
    lastName = db.StringProperty()
    locale = db.StringProperty()
    verified = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    lastLogin = db.DateTimeProperty(auto_now=True)
    

def zipcode_key(zipcode_value=None):
  """Constructs a datastore key for a Zipcode entity with zipcode_value."""
  return db.Key.from_path('Zipcode', zipcode_value or 'default_zipcode')

def user_key(user_name=None):
  """Constructs a datastore key for a Action entity with action_name."""
  return db.Key.from_path('UserNC', user_name or 'default_action')

def send_welcome_email(toEmail, toName):
    """ This function sends a welcome email to new users """
    message = mail.EmailMessage(sender="NextClimate <info@nextclimate.org>",
				subject="Welcome to NextClimate")
    message.to = toEmail
    message.body = """
    Dear %s,

    We are glad you've signed up to be a NextClimate user. We
    look forward to helping you and your community achieve your
    climate change mitigation goals.

    If you've found this service useful, let your friends know
    by pointing them to www.nextclimate.org.

    Your suggestions are welcome -- just hit reply to this email!

    The NextClimate Team
    """ % (toName)
    message.send()




# this class gets called when there is a request to /zip_query
# it queries the datastore and pulls the city, state, and climate
# info. It then constructs the text that is displayed
# comparing the future climate of this location to the present
# climate of a current location. Finally, this is packaged in the variable
# named template and pushed to 
class AuthUserPage(webapp.RequestHandler):

    def post(self):
	# the welcome page does a form post with the user's info. This is
	# implemented as a hidden form on the welcome page.
	# the fields are populated from facebook data.
	# Here, check to see if the user is already in our database and if
	# not, add the user.
	
	# first check to see if this is a new users and if so add this user to
	# the database

	
	user_query = UserNC.all()
	user_query.filter("FBid = ",self.request.get('id'))

	if not user_query.count(limit=1):
	    # case where this id is not in the database,
	    # so add this user

	    new_user = UserNC(parent=user_key('99999'))

	    new_user.name = self.request.get('name')
	    new_user.FBid = self.request.get('id')
	    new_user.gender = self.request.get('gender')
	    new_user.email = db.Email(self.request.get('email'))

	    try:
		d = datetime.datetime.strptime(self.request.get('birthday'),"%m/%d/%Y").date()
	    except:
		d = None
	    new_user.birthday = d
	    new_user.firstName = self.request.get('first_name')
	    new_user.lastName = self.request.get('last_name')
	    new_user.locale = self.request.get('locale')
	    new_user.verified = self.request.get('verified')
	    #new_user.created = datetime.datetime.today()
	    #new_user.lastLogin = datetime.datetime.today()
	    
	    new_user.put()

	    send_welcome_email(new_user.email, new_user.name)
	    # could put an else clause here to update the lastLogin.

	# go back to the actnow page; eventually update this so other pages can re-direct here.
	self.redirect('/actnow?zipcode='+self.request.get('zipcode') + '&id='+self.request.get('id'))


    # execute this code at a get request
    def get(self):
	
        access_token = self.request.get('access_token')
	if (access_token == ''):
	    template_values={'accessToken':'none'}
	    template_values={'zipcode':self.request.get('zipcode')}
	    path = os.path.join(os.path.dirname(__file__), 'authUser.html')
	    self.response.out.write(template.render(path, template_values))
	else:
	    fb_response = urllib.urlopen('https://graph.facebook.com/me?'+access_token)
	    fb_text = fb_response.read(-1)
	    fb_json = open('fb_text')
	    fb_data = json.loads(fb_json)
	    template_values={'userId':fb_data["id"], 'userName':fb_data["name"], 'accessToken':access_token, 'zipcode':self.request.get('zipcode')}
	    fb_data.close()
	    path = os.path.join(os.path.dirname(__file__), 'authUser.html')
	    self.response.out.write(template.render(path, template_values))



