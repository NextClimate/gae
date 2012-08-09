
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
from google.appengine.api import mail
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
  savings =  db.StringProperty()
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

# this class is a connection between a user and and action
class UserAction(db.Model):
  name = db.StringProperty() # the user name that has started a project
  locale = db.StringProperty() # locale, like "en_US" for language support
  FBid = db.StringProperty() # the user that has started a project
  email = db.StringProperty() # the email address of the user
  actionName = db.StringProperty() # name of the action
  dateStart = db.DateTimeProperty(auto_now_add=True) # date project was started
  dateEnd = db.DateTimeProperty() # date project was completed
  complete = db.StringProperty() # one of started or complete

def user_action_key(user_action_name=None):
  """Constructs a datastore key for a UserAction entity with user_action_name."""
  return db.Key.from_path('UserAction', user_action_name or 'default_action')


def send_start_email(toEmail, toName, actionName):
    """ This function sends an email when a user starts a new action """
    message = mail.EmailMessage(sender="NextClimate <info@nextclimate.org>",
				subject=actionName)
    message.to = toEmail
    message.body = """
    Dear %s,

    Congrats on starting a new project, %s.

    We look forward to helping you achieve your energy efficiency
    goals. We'll follow up with you in a few days to see how it is
    going.

    If you've found this service useful, let your friends know
    by pointing them to www.nextclimate.org.

    Your suggestions are welcome -- just hit reply to this email!

    The NextClimate Team
    """ % (toName, actionName)
    message.send()


def send_complete_email(toEmail, toName, actionName):
    """ This function sends an email when a user starts a new action """
    message = mail.EmailMessage(sender="NextClimate <info@nextclimate.org>",
				subject=actionName)
    message.to = toEmail
    message.body = """
    Dear %s,

    Congrats on completing this project, %s!

    If you've found this service useful, let your friends know
    by pointing them to www.nextclimate.org.

    Your suggestions are welcome -- just hit reply to this email!

    The NextClimate Team
    """ % (toName, actionName)
    message.send()


# this class is called when there is a request to /selectAct
# it populates the selectAct.html page with the action information
# for the energy saving action that the users has selected.

class SelectActPage(webapp.RequestHandler):
    def get(self):
	start_boolean = bool(self.request.get('start'))
	FBid = self.request.get('id')
	
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

	    # check to see if user has already started this action
	    userAction_query = UserAction.all()
	    userAction_query.filter("FBid = ",FBid)
	    userAction_query.filter("actionName = ",act_value)

	    if not userAction_query.count(limit=1):
		status = "new"
		start_text ="Click Start to begin this project"
	    else:
		uA = userAction_query.fetch(1)
		status = uA[0].complete
		if status == "started":
		    start_text="You have started this project"
		if status == "complete":
		    start_text="You have completed this project"


	    template_values = {
		'status':status,
		'startText':start_text,
		'selectName':v.name,
		'selectDesc':v.description,
		'selectYoutube':v.youtube,
		'selectChecklist':string.split(v.checklist,"|"),
		'selectType':act_value,
		'selectMessage':'Hi, I am starting a project to improve my home\'s energy efficiency. Do you have a '+string.split(v.checklist,"|")[0].lower()+' that I could borrow?'
		}

	path = os.path.join(os.path.dirname(__file__), 'selectAct.html')	    	
        self.response.out.write(template.render(path, template_values))

    def post(self):
	start_boolean = bool(self.request.get('start'))
	complete_boolean = bool(self.request.get('complete'))

	if start_boolean:
	    status = "started"
	    start_text="You have started this project"	    
	    # pull user info from web request
	    email = self.request.get('email')
	    name = self.request.get('name')
	    actionName = self.request.get('actionName')
	    FBid = self.request.get('id')

	    # check to see if user has already started this project
	    userAction_query = UserAction.all()
	    userAction_query.filter("FBid = ",FBid)
	    userAction_query.filter("actionName = ",actionName)

	    if not userAction_query.count(limit=1):
		new_user_action = UserAction(parent=user_action_key('99999'))
		new_user_action.name = name
		new_user_action.FBid = FBid
		new_user_action.email = email
		new_user_action.actionName = actionName
		new_user_action.locale = self.request.get('locale')
		new_user_action.complete = "started"
		new_user_action.put()

		# also need to send an email to the user
		send_start_email(email, name, actionName)

	if complete_boolean:
	    status = "complete"
	    start_text="You have completed this project"	    
	    # pull user info from web request
	    email = self.request.get('email')
	    name = self.request.get('name')
	    actionName = self.request.get('actionName')
	    FBid = self.request.get('id')

	    # check to see if user has already started this project
	    userAction_query = UserAction.all()
	    userAction_query.filter("FBid = ",FBid)
	    userAction_query.filter("actionName = ",actionName)

	    mod_user_action = userAction_query.fetch(1)[0]
	    mod_user_action.complete = "complete"
	    mod_user_action.put()

	    # also need to send an email to the user
	    send_complete_email(email, name, actionName)





	# query action database to repopulate the action contect
        # this could be improved to have the post command repost all this info
	# to avoid a database query

        act_value=self.request.get('type')
 	qTrue = 0
 	if (len(act_value) > 0):
 	     qTrue = 1

	# query the datastore for matching action
        action_query = Action.all()
        actions = action_query.filter("name =",act_value)
	results = actions.fetch(1)

	# if valid results, populate template that is sent to selectAct.html
	for v in results:
	    template_values = {
		'status':status,
		'startText':start_text,
		'selectName':v.name,
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

