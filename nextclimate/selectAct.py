
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


# this entity in the datastore includes the information
# about an energy-saving action. So far, all that
# have been populated are the name, youtube url, description,
# and checklist
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
  # one of DIY, sponsors, store, offsets
  savings =  db.FloatProperty()
  category = db.StringProperty() 
  #for DIY
  youtube = db.StringProperty()
  checklist = db.StringProperty()
  #for sponsors
  sponsors = db.StringProperty()
  # for store
  storeURL = db.StringProperty()


def action_key(action_name=None):
  """Constructs a datastore key for a Action entity with action_name."""
  return db.Key.from_path('Action', action_name or 'default_action')



# this class is called when there is a request to /selectAct
# it populates the selectAct.html page with the action information
# for the energy saving action that the users has selected.

class SelectActPage(webapp.RequestHandler):
    def get(self):
        act_value=self.request.get('type')
 	qTrue  = 0
 	if (len(act_value) > 0):
 	     qTrue = 1

	# query the datastore for matching action
        action_query = Action.all()
        actions = action_query.filter("name =",act_value)
	results = actions.fetch(1)

	# if valid results, populate template that is sent to selectAct.html
	for v in results:
	    template_values = {'selectName':v.name,
	    'selectDesc':v.description,
	    'selectYoutube':v.youtube,
	    'selectChecklist':string.split(v.checklist,"|"),
	    'selectType':act_value,
	    'selectMessage':'Hi, I am starting a project to improve my home\'s energy efficiency. Do you have a '+string.split(v.checklist,"|")[0].lower()+' that I could borrow?'
	    }

	path = os.path.join(os.path.dirname(__file__), 'selectAct.html')	    	
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/selectAct', SelectActPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

