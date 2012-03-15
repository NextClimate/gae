
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


class ZipMSA(db.Model):
  """Models an individual zipcode associated with a metropolitan area"""
  zipcode=db.StringProperty()
  MSA = db.StringProperty(multiline=False)  

def zipmsa_key(zipmsa_value=None):
  """Constructs a datastore key for a Zipcode entity with zipcode_value."""
  return db.Key.from_path('ZipMSA', zipmsa_value or 'default_zipcode')



class ActNowPage(webapp.RequestHandler):
    def get(self):
        zipcode_value=self.request.get('zipcode_value')
# 	qTrue  = 0
# 	if (len(zipcode_value) > 0):
# 	    qTrue = 1
#         zipcode_query = Zipcode.all()
#         zipcodes = zipcode_query.filter("zipcode =",zipcode_value)
# 	results = zipcodes.fetch(1)
# 	place = "not good"
	template_values = {}
# 	    template_values = {
# 	    'qTrue':range(qTrue),
#             'zipcode': v.zipcode,
# 	    'city': string.capwords(v.city),
# 	    'state': v.state,
# 	    'maxTobs_1990': v.maxTobs_1990,
# 	    'maxTa1_2050':v.maxTa1_2050,
# 	    'maxTa1_2090':v.maxTa1_2090,	    
# 	    'maxTb2_2090':v.maxTb2_2090,	    
#              'place': place,
# 	     }

        path = os.path.join(os.path.dirname(__file__), 'actnow.html')
        self.response.out.write(template.render(path, template_values))

	#class ZipcodeShow(webapp.RequestHandler):
	#def 


application = webapp.WSGIApplication([
  ('/actnow', ActNowPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

