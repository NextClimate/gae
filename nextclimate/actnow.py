
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


# this class is called when there is a request to /actnow page.
# it renders userInfo.html, which asks the user a series of
# questions about energy use in order to develop an energy profile
# that is specific to this user. The user is then directed to
# /energy to look at the impact of their energy choices.

class ActNowPage(webapp.RequestHandler):
    def get(self):
        zipcode_value=self.request.get('zipcode_value')
        FBid=self.request.get('id')

	template_values = {'zipcode':zipcode_value}

	path = os.path.join(os.path.dirname(__file__), 'userInfo.html')
	
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([
  ('/actnow', ActNowPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

