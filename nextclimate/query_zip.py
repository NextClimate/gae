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
class QueryZipPage(webapp.RequestHandler):

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

	# go back to the query_zip page
	self.redirect('/queryZip')


    # execute this code at a get request
    def get(self):
	
	# parse the zip code value out of the URL
        zipcode_value=self.request.get('zipcode_value')
	qTrue  = False
	if (len(zipcode_value) > 0):
	    qTrue = True

	# query the datastore, retrieve the record with this zipcode 
        zipcode_query = Zipcode.all()
        zipcodes = zipcode_query.filter("zipcode =",zipcode_value)
	results = zipcodes.fetch(1)

	# initialize values
	place = "not good"
	template_values = {}

	# iterate through results, although there should be only 1
	# check the number of days to exceed 90 degrees and 
	# assign a place that is like that in current conditions.
	# this generates text 'the future climate of you city will
	# be most like this place in the present day'
	for v in results:
	    p1 = "The future temperatures of "+string.capwords(v.city)+" will be most like present day "
	    if v.maxTa1_2090 > 0:
		place = p1 + "Los Angeles"
	    if v.maxTa1_2090 > 10:
		place = p1 + "Los Angeles"
	    if v.maxTa1_2090 > 20:
		place = p1 + "Kansas"
	    if v.maxTa1_2090 > 30:
		place = p1 + "Missouri"		
	    if v.maxTa1_2090 > 40:
		place = p1 + "Jackson, Mississippi"
	    if v.maxTa1_2090 > 50:
		place = p1 + "New Orleans, Louisiana"
	    if v.maxTa1_2090 > 60:
		place = p1 + "Dallas, Texas"
	    if v.maxTa1_2090 > 80:
		place = p1 + "Sacramento, California"
	    if v.maxTa1_2090 > 90:
		place = p1 + "Orlando, Florida"
	    if v.maxTa1_2090 > 100:
		place = p1 + "Palm Springs, California"
	    if v.maxTa1_2090 > 120:
		place = p1 + "Brownsville, Texas"
	    if v.maxTa1_2090 > 140:
		place = p1 + "Las Vegas, Nevada"
	    if v.maxTa1_2090 > 160:
		place = p1 + "Phoenix, Arizona"
	    if v.maxTa1_2090 > 180:
		place = "The number of days above 90 degrees in your area will be greater than any place in the present-day continental US"

	    # fill in these template values. These variables are passed to
	    # the webpage and rendered on the page. Look for variables of
	    # the form {{varname}} in the html; these values replace those {{}}
	    # placeholders
	    template_values = {
	    'qTrue':qTrue,
            'zipcode': v.zipcode,
	    'city': string.capwords(v.city),
	    'state': v.state,
	    'maxTobs_1990': v.maxTobs_1990,
	    'maxTa1_2050':v.maxTa1_2050,
	    'maxTa1_2090':v.maxTa1_2090,	    
	    'maxTb2_2090':v.maxTb2_2090,	    
             'place': place,
	     }

	# return the file query_zip.html, with all of the template
	# values replaced with the data assigned above
        path = os.path.join(os.path.dirname(__file__), 'query_zip.html')
        self.response.out.write(template.render(path, template_values))

	#class ZipcodeShow(webapp.RequestHandler):
	#def 


