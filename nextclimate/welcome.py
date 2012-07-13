
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


# this class gets called when there is a get request to url '/'
# it simply returns the welcome.html file
# all the login / facebook is handled with javascript on the page
class WelcomePage(webapp.RequestHandler):
    def get(self):
	template_values={}
	path = os.path.join(os.path.dirname(__file__), 'welcome.html')
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([
  ('/', WelcomePage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

