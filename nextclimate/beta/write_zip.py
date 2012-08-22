
import os
from google.appengine.ext.webapp import template

import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class Zipcode(db.Model):
  """Models an individual zipcode associated with climate change values"""
  zipcode=db.StringProperty()
  city = db.StringProperty(multiline=False)
  state = db.StringProperty(multiline=False)
  maxTobs_1950 = db.IntegerProperty()
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
        zipcode_query = Zipcode.all()
        zipcodes = zipcode_query.fetch(10)

#         if users.get_current_user():
#             url = users.create_logout_url(self.request.uri)
#             url_linktext = 'Logout'
#         else:
#             url = users.create_login_url(self.request.uri)
#             url_linktext = 'Login'

        template_values = {
	      'zipcodes': zipcodes,
#             'url': url,
#             'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'write_zip.html')
        self.response.out.write(template.render(path, template_values))

	#class ZipcodeShow(webapp.RequestHandler):
	#def 



class ZipcodePut(webapp.RequestHandler):

  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    #    guestbook_name = self.request.get('guestbook_name')
    zipcode = Zipcode(parent=zipcode_key('99999'))

    #    if users.get_current_user():
    #  greeting.author = users.get_current_user()

    zipcode.zipcode = self.request.get('zipcode')
    zipcode.city = self.request.get('city')
    zipcode.state = self.request.get('state')
    zipcode.maxTobs_1950 = 9
    zipcode.maxTobs_1990 = 9
    zipcode.maxTa1_2050 = 9
    zipcode.maxTa1_2090 = 9
    zipcode.maxTb2_2090 = 9

    zipcode.put()
    self.redirect('/write_zip?zipcode_value=99999')


application = webapp.WSGIApplication([
  ('/write_zip', MainPage),
  ('/addEntry', ZipcodePut)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

