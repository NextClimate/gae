
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

def zipcode_key(zipcode_value=None):
  """Constructs a datastore key for a Zipcode entity with zipcode_value."""
  return db.Key.from_path('Zipcode', zipcode_value or 'default_zipcode')


# this class gets called when ther is a request to /zip_query
# it queries the datastore and pulls the city, state, and climate
# info. It then constructs the text that is displayed
# comparing the future climate of this location to the present
# climate of a current location. Finally, this is packaged in the variable
# named template and pushed to 
class MainPage(webapp.RequestHandler):

    # execute this code at a get request
    def get(self):
	
	# parse the zip code value out of the URL
        zipcode_value=self.request.get('zipcode_value')
	qTrue  = 0
	if (len(zipcode_value) > 0):
	    qTrue = 1

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
	    p1 = "The future climate of "+string.capwords(v.city)+" will be most like present day "
	    if v.maxTa1_2090 > 0:
		place = p1 + "Upstate New York"
	    if v.maxTa1_2090 > 10:
		place = p1 + "New York City"
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
		place = "The climate in your area will be warmer than any place in the present-day continental US"

	    # fill in these template values. These variables are passed to
	    # the webpage and rendered on the page. Look for variables of
	    # the form {{varname}} in the html; these values replace those {{}}
	    # placeholders
	    template_values = {
	    'qTrue':range(qTrue),
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


application = webapp.WSGIApplication([
  # for url /queryZip, instantiate an instance of MainPage, defined above
  ('/queryZip', MainPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

