
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


# this is a class for mapping zip codes to MSA (metro areas)
# this is not used yet, but at some point, it would likely
# make sense to show people data in their MSA, rather
# than zip code.

class ZipMSA(db.Model):
  """Models an individual zipcode associated with a metropolitan area"""
  zipcode=db.StringProperty()
  MSA = db.StringProperty(multiline=False)  

def zipmsa_key(zipmsa_value=None):
  """Constructs a datastore key for a Zipcode entity with zipcode_value."""
  return db.Key.from_path('ZipMSA', zipmsa_value or 'default_zipcode')


# this class gets called when ther is a request to /energy
# it pulls the answers to the questions fron the /actnow
# page out of the http post request. This includes the
# zipcode and the electricity use. The heating use is
# not currently included in the calculation. The electricity
# use is handled in a very crude way. This needs to
# be improved. 
#

class ActNowPage(webapp.RequestHandler):
    def post(self):
        zipcode_value=self.request.get('zipcode')
        electricity=self.request.get('electricity')
	heat=self.request.get('heat')

	# elecMod is a modifier that is based on the user response
	# it modifies the size of the users energy use
	# if the user picks the low value, it is 0.5,
	# if the user picks the high value, it is 1.5,
	# otherwise, just 1.0
	
	elecMod = 1.0
	if electricity == "low": elecMod = 0.5
	if electricity == "high": elecMod = 1.5	    


	# get this location info to make the results more
	# personal. Right now, this just makes the labels
	# have the city name, but could impact the calculation,
	# for example, Ohio uses more carbon intensive fuels
	# for energy production, while Oregon uses more hydro.
	    
  	if (len(zipcode_value) > 0):
         zipcode_query = Zipcode.all()
         zipcodes = zipcode_query.filter("zipcode =",zipcode_value)
	 results = zipcodes.fetch(1)

	 if (len(results)>0):
	     city = string.capwords(results[0].city)
	 else:
	     city = 'your area'
	     

	template_values = {'zipcode':zipcode_value,
			   'city':city,
			   'electricity': electricity,
			   'elecMod': elecMod}


	# there are more calculations in the javascript in energy.html
 	# user is shown what is in energy.html
	path = os.path.join(os.path.dirname(__file__), 'energy.html')
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([
  ('/energy', ActNowPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

