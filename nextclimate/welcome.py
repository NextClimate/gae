
import os

import cgi
import datetime
import urllib
import wsgiref.handlers
import string
#import json

import webapp2
from webapp2_extras import routes

#from django.utils import simplejson
from google.appengine.ext import db
from google.appengine.api import users
#from google.appengine.ext import webapp2
#from google.appengine.ext.webapp.util import run_wsgi_app


# this class gets called when there is a get request to url '/'
# it simply returns the welcome.html file
# all the login / facebook is handled with javascript on the page
class WelcomePage(webapp2.RequestHandler):
    def get(self):

	self.response.headers.add_header("Access-Control-Allow-Origin", "*")
	
	uastring = self.request.headers.get('user_agent')
	if "MSIE 6.0" in uastring or  "MSIE 6." in uastring:
	    self.response.out.write("<html><body>"+uastring+"\n<p>We are sorry. The NextClimate tools are not compatible with your browser. We suggest you upgrade to a more recent release of Internet Explorer. Or try browsing the web with <a href='http://mozilla.org'>Firefox</a> (it's free and we think you'll like it).</p></body></html>")
	else:
	    path = os.path.join(os.path.dirname(__file__), 'welcome.html')
	    f = open(path)
	    self.response.out.write(f.read())
	
            

import beta.base
import query_zip
import beta.query_zip
import actnow
import beta.actnow
import energy
import beta.energy
import selectAct
import beta.selectAct
import authUser
import beta.authUser
import offset
import beta.offset
import beta.api
import api



app = webapp2.WSGIApplication([
    routes.DomainRoute('www.nextclimate.org', [
	webapp2.Route('/queryZip/<zipcode_value>/', handler=query_zip.QueryZipPage, name='zipcode_value'),
	webapp2.Route('/queryZip', handler=query_zip.QueryZipPage, name='zipcode_value'),
	webapp2.Route('/authUser', handler=authUser.AuthUserPage), 
	webapp2.Route('/actnow', handler=actnow.ActNowPage),
	webapp2.Route('/energy', handler=energy.EnergyPage),
	webapp2.Route('/selectAct', handler=selectAct.SelectActPage),
	webapp2.Route('/offset', handler=offset.OffsetPage),
	webapp2.Route('/api', handler=api.Temperature), 
	webapp2.Route('/mail', handler=mailPage), 
	webapp2.Route('/', handler=WelcomePage, name='home'),



	]),
	webapp2.Route('/queryZip/<zipcode_value>/', handler=beta.query_zip.QueryZipPage, name='zipcode_value'),
	webapp2.Route('/queryZip', handler=beta.query_zip.QueryZipPage, name='zipcode_value'),
	webapp2.Route('/api', handler=beta.api.Temperature), 
	webapp2.Route('/authUser', handler=beta.authUser.AuthUserPage), 
	webapp2.Route('/actnow', handler=beta.actnow.ActNowPage),
	webapp2.Route('/energy', handler=beta.energy.EnergyPage),
	webapp2.Route('/selectAct', handler=beta.selectAct.SelectActPage),
	webapp2.Route('/offset', handler=beta.offset.OffsetPage),
	webapp2.Route('/', handler=beta.base.WelcomePage, name='home'),

    ])



#     routes.DomainRoute('<subdomain>.app-id.appspot.com', [
# 	webapp2.Route('/', handler=SubdomainHomeHandler, name='subdomain-home'),
# 	]),
# 	webapp2.Route('/', handler=HomeHandler, name='home'),
#     ])


# app = {
#     'localhost:8081': webapp2.WSGIApplication([('/', beta.base.WelcomePage),
# 					      ('/queryZip', beta.query_zip.QueryZipPage),
# 					      (r'/queryZip/[0-9]{5}/', beta.query_zip.QueryZipPage),
# 					      ('/api', beta.api.Temperature),
# 					      ('/authUser', beta.authUser.AuthUserPage), 
# 					      ('/actnow', beta.actnow.ActNowPage),
# 					      ('/energy', beta.energy.EnergyPage),
# 					      ('/selectAct', beta.selectAct.SelectActPage),
# 					      ('/offset', beta.offset.OffsetPage)					      
# 					      ]),
#     'www.nextclimate.org': webapp2.WSGIApplication([('/', WelcomePage),
# 						   ('/queryZip', query_zip.QueryZipPage),
# 						   (r'/queryZip/[0-9]{5}/', query_zip.QueryZipPage),
# 						   ('/authUser', authUser.AuthUserPage), 
# 						   ('/actnow', actnow.ActNowPage),
# 						   ('/energy', energy.EnergyPage),
# 						   ('/selectAct', selectAct.SelectActPage),
# 						   ('/offset', offset.OffsetPage)					      
# 						   ]),
#     'beta.nextclimate.org': webapp2.WSGIApplication([('/', beta.base.WelcomePage),
# 						    ('/queryZip', beta.query_zip.QueryZipPage),
# 						    (r'/queryZip/[0-9]{5}/', beta.query_zip.QueryZipPage),
# 						    ('/api', beta.api.Temperature),
# 						    ('/authUser', beta.authUser.AuthUserPage), 
# 						    ('/actnow', beta.actnow.ActNowPage),
# 						    ('/energy', beta.energy.EnergyPage),
# 						    ('/selectAct', beta.selectAct.SelectActPage),
# 						    ('/offset', beta.offset.OffsetPage)					      
# 						    ])
# }

# def main():
#     run_wsgi_app(applications[os.environ['HTTP_HOST']])

# if __name__ == '__main__':
#   main()
