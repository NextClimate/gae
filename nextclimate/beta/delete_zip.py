
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


class DeletePage(webapp.RequestHandler):
    def get(self):

	c = 0
	while True:
	    zipcode_query = Zipcode.all()
	    e = zipcode_query.fetch(1000)
	    if e:
		c = c + len(e)
		db.delete(e)
	    else:
		break



#         if users.get_current_user():
#             url = users.create_logout_url(self.request.uri)
#             url_linktext = 'Logout'
#         else:
#             url = users.create_login_url(self.request.uri)
#             url_linktext = 'Login'

        template_values = {
            'del_count': c,
#             'url': url,
#             'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'delete.html')
        self.response.out.write(template.render(path, template_values))

	#class ZipcodeShow(webapp.RequestHandler):
	#def 


application = webapp.WSGIApplication([
  ('/delete', DeletePage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

