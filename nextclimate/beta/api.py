import os
import webapp2
import jinja2

import cgi
import datetime
import urllib
import wsgiref.handlers
import string
import re

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail



# import sys, urllib, string, SOAPpy
# from xml.sax import parse, ContentHandler, SAXParseException
# from SOAPpy import SOAPProxy
# from SOAPpy import *





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


def zipcode_key(zipcode_value=None):
  """Constructs a datastore key for a Zipcode entity with zipcode_value."""
  return db.Key.from_path('Zipcode', zipcode_value or 'default_zipcode')

def user_key(user_name=None):
  """Constructs a datastore key for a Action entity with action_name."""
  return db.Key.from_path('UserNC', user_name or 'default_action')




# this class gets called when there is a request to /zip_query
# it queries the datastore and pulls the city, state, and climate
# info. It then constructs the text that is displayed
# comparing the future climate of this location to the present
# climate of a current location. Finally, this is packaged in the variable
# named template and pushed to 
class Temperature(webapp2.RequestHandler):

    def get(self):
	
	# parse the zip code value out of the URL
        zipcode_value=self.request.get('zipcode_value')
	qTrue  = False
	if (len(zipcode_value) > 0):
	    qTrue = True
	else:
	    zipcode_value=self.request.get('zip_code')
	    if (len(zipcode_value) > 0):
		qTrue = True
	    else:
		zipcode_value = re.findall("[0-9]{5}", self.request.path)[0]
		if (len(zipcode_value) == 5):
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
		place = "The number of days above 90 degrees in %s will be greater than any place in the present-day US" % (string.capwords(v.city))

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

	      

	     #path = os.path.join(os.path.dirname(__file__), 'query_zip.html')
	     #self.response.out.write(template.render(path, template_values))

	     #	    from django.utils import simplejson
	    import json
	    self.response.headers['Content-Type'] = 'application/json'
	    jsonData = template_values
	    self.response.out.write(json.dumps(jsonData))

	    #	    print 'Content-Type: text/plain'
	    #print ''
	    #print 'Hello, ' + v.city




