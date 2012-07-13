
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


class Action(db.Model):
  """Models an Action to reduce greenhouse gases """
  name=db.StringProperty()
  locale=db.StringProperty()
  description=db.StringProperty()
  effectHeatCool = db.FloatProperty()
  effectWater = db.FloatProperty()
  effectLighting = db.FloatProperty()
  effectAppliance = db.FloatProperty()
  cost = db.FloatProperty()
  savings =  db.FloatProperty()
  # one of DIY, sponsors, store, offsets
  category = db.StringProperty() 
  # for DIY 
  youtube = db.StringProperty()
  checklist = db.StringProperty()
  # for sponsors
  sponsors = db.StringProperty()
  # for store
  storeURL = db.StringProperty()


def action_key(action_name=None):
  """Constructs a datastore key for a Action entity with action_name."""
  return db.Key.from_path('Action', action_name or 'default_action')

class MainPage(webapp.RequestHandler):
    def get(self):
        action_name=self.request.get('action_name')
        action_query = Action.all()
        actions = action_query.fetch(10)

#         if users.get_current_user():
#             url = users.create_logout_url(self.request.uri)
#             url_linktext = 'Logout'
#         else:
#             url = users.create_login_url(self.request.uri)
#             url_linktext = 'Login'

        template_values = {
	      'actions': actions,
#             'url': url,
#             'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'write_act.html')
        self.response.out.write(template.render(path, template_values))


class ActionPut(webapp.RequestHandler):

  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    #    guestbook_name = self.request.get('guestbook_name')
    action = Action(parent=action_key('99999'))

    #    if users.get_current_user():
    #  greeting.author = users.get_current_user()

    action.name = self.request.get('name')
    action.description = self.request.get('description')
    action.youtube = self.request.get('youtube')
    action.checklist=self.request.get('checklist')

    action.put()
    self.redirect('/write_act?action_value=99999')


application = webapp.WSGIApplication([
  ('/write_act', MainPage),
  ('/addActEntry', ActionPut)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

