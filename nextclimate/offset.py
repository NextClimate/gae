
import os
from google.appengine.ext.webapp import template

import cgi
import datetime
import urllib
import urllib2

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp.util import run_wsgi_app



class OffsetPage(webapp.RequestHandler):
    def get(self):

	qty = self.request.get('qty')	
	self.redirect('''http://store.terrapass.com/store/p/56-TerraPass-carbon-offsets-1-000lbs.html?qty=%s''' % (qty))
	





