
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

class MainPage(webapp.RequestHandler):
    def get(self):
        zipcode_value=self.request.get('zipcode_value')
	qTrue  = 0
	if (len(zipcode_value) > 0):
	    qTrue = 1
        zipcode_query = Zipcode.all()
        zipcodes = zipcode_query.filter("zipcode =",zipcode_value)
	results = zipcodes.fetch(1)
	place = "not good"
	template_values = {}
	p1 = "The future climate of your area will be most like present day "
	for v in results:
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

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

	#class ZipcodeShow(webapp.RequestHandler):
	#def 


application = webapp.WSGIApplication([
  ('/', MainPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

