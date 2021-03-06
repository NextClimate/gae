
import os
from google.appengine.ext.webapp import template

import cgi
import datetime
import urllib
import wsgiref.handlers
import string
#import json

from django.utils import simplejson
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


# this class gets called when there is a get request to url '/'
# it simply returns the welcome.html file
# all the login / facebook is handled with javascript on the page
class WelcomePage(webapp.RequestHandler):
    def get(self):

        access_token = self.request.get('access_token')
	if (access_token == ''):
	    template_values={'accessToken':'none'}
	    path = os.path.join(os.path.dirname(__file__), 'welcome.html')
	    self.response.out.write(template.render(path, template_values))
	else:
	    fb_response = urllib.urlopen('https://graph.facebook.com/me?'+access_token)
	    fb_text = fb_response.read(-1)
	    fb_json = open('fb_text')
	    fb_data = json.loads(fb_json)
	    template_values={'userId':fb_data["id"], 'userName':fb_data["name"], 'accessToken':access_token}
	    fb_data.close()
	    path = os.path.join(os.path.dirname(__file__), 'welcome.html')
	    self.response.out.write(template.render(path, template_values))
	
class BetaWelcomePage(webapp.RequestHandler):
    def get(self):

        access_token = self.request.get('access_token')
	if (access_token == ''):
	    template_values={'accessToken':'none'}
	    path = os.path.join(os.path.dirname(__file__), 'beta/welcome.html')
	    self.response.out.write(template.render(path, template_values))
	else:
	    fb_response = urllib.urlopen('https://graph.facebook.com/me?'+access_token)
	    fb_text = fb_response.read(-1)
	    fb_json = open('fb_text')
	    fb_data = json.loads(fb_json)
	    template_values={'userId':fb_data["id"], 'userName':fb_data["name"], 'accessToken':access_token}
	    fb_data.close()
	    path = os.path.join(os.path.dirname(__file__), 'beta/welcome.html')
	    self.response.out.write(template.render(path, template_values))
	

# application = webapp.WSGIApplication([
#   ('/', WelcomePage)
# ], debug=True)


# def main():
#   run_wsgi_app(application)

import beta.base

applications = {
    'localhost:8081': webapp.WSGIApplication([('/', v002.base.WelcomePage)]),
    'www.nextclimate.org': webapp.WSGIApplication([('/', WelcomePage)]),
    'beta.nextclimate.org': webapp.WSGIApplication([('/', beta.base.WelcomePage)])
}

def main():
    run_wsgi_app(applications[os.environ['HTTP_HOST']])

if __name__ == '__main__':
  main()
