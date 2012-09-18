
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


# this class holds information about energy saving actions
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


# this class holds a zip code and climate info. This is an
# entity in the datastore.

class Zipcode(db.Model):
  """Models an individual zipcode associated with climate change values"""
  zipcode=db.StringProperty()
  city = db.StringProperty(multiline=False)
  state = db.StringProperty(multiline=False)
  maxTobs_1990 = db.IntegerProperty()
  maxTa1_2050 = db.IntegerProperty()
  maxTa1_2090 = db.IntegerProperty()    
  maxTb2_2090 = db.IntegerProperty()
    
def zipcode_key(zipcode_value=None):
  """Constructs a datastore key for a Zipcode entity with zipcode_value."""
  return db.Key.from_path('Zipcode', zipcode_value or 'default_zipcode')


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


# this class gets called when ther is a request to /energy
# it pulls the answers to the questions fron the /actnow
# page out of the http post request. This includes the
# zipcode and the electricity use. The heating use is
# not currently included in the calculation. The electricity
# use is handled in a very crude way. This needs to
# be improved. 
#

class EnergyPage(webapp.RequestHandler):
    def get(self):
        zipcode_value=self.request.get('zipcode')
        electricity=self.request.get('electricity')
	heat=self.request.get('heat')
	FBid=self.request.get('id')
	
	# elecMod is a modifier that is based on the user response
	# it modifies the size of the users energy use
	# if the user picks the low value, it is 0.5,
	# if the user picks the high value, it is 1.5,
	# otherwise, just 1.0
	
	elecMod = 1.0
	if electricity == "low": elecMod = 0.5
	if electricity == "high": elecMod = 1.5	    


	# get this location info to make the results more
	# personal. Right now, this just makes the labels
	# have the city name, but could impact the calculation,
	# for example, Ohio uses more carbon intensive fuels
	# for energy production, while Oregon uses more hydro.
	    
  	if (len(zipcode_value) > 0):
         zipcode_query = Zipcode.all()
         zipcodes = zipcode_query.filter("zipcode =",zipcode_value)
	 results = zipcodes.fetch(1)

	 if (len(results)>0):
	     city = string.capwords(results[0].city)
	 else:
	     city = 'your area'


	# pull all of the actions from the table
	# and assemble into a javascript array.
	# Need some logic here to rank results to
        # show top five most relevant.

	action_query = Action.all()
	actions = action_query.fetch(5)
	energy_list = ""

	# has the user started/completed these actions?

	userAction_query = UserAction.all()
	userAction_query.filter("FBid = ",FBid)
	userActions = userAction_query.fetch(5)

	heatCoolMod = 1
	waterMod = 1
	lightingMod = 1
	applianceMod = 1

    
	countAction = 0
	script_all = """<script type="text/javascript">\n """
	# iterate over all actions
	for a in actions:
	    # for each action, check if user has started it
	    for ua in userActions:
		countAction = countAction + 1
		if (ua.actionName == a.name) and (ua.complete == "started"):
		    script_html = """ function selectAct%d() {window.location.href='/selectAct?id=%s&type=%s&zipcode=%s&electricity=%s&heat=%s';};\n """ % (countAction, FBid, a.name, zipcode_value, electricity, heat)
		    script_all = script_all + script_html
		    button_html = """<button style='width:90px' onclick='selectAct%d()'>%s</button>""" % (countAction, "Finish It")
		    energy_list = energy_list + """[ '%s',%f, %f, %f, %f, '%s', "%s", %d],""" % (a.name, a.effectHeatCool, a.effectWater, a.effectLighting, a.effectAppliance, a.savings, button_html, 0)
		    break
		if (ua.actionName == a.name) and (ua.complete == "complete"):
		    button_html = "<span style='text-align:center;width:90px'>Complete!<span>"
		    energy_list = energy_list + """[ '%s',%f, %f, %f, %f, '%s', "%s", %d],""" % (a.name, 1, 1, 1, 1, a.savings, button_html, 1)
		    heatCoolMod = heatCoolMod * a.effectHeatCool
		    waterMod = waterMod * a.effectWater
		    lightingMod = lightingMod * a.effectLighting
		    applianceMod = applianceMod * a.effectAppliance
		    break
	    else:
		script_html = """ function selectAct%d() {window.location.href='/selectAct?id=%s&type=%s&zipcode=%s&electricity=%s&heat=%s';};\n """ % (countAction, FBid, a.name, zipcode_value, electricity, heat)
		script_all = script_all + script_html
		button_html = """<button style='width:90px' onclick='selectAct%d()'>%s</button>""" % (countAction, "Learn more")

		energy_list = energy_list + """[ '%s',%f, %f, %f, %f, '%s', "%s", %d],""" % (a.name, a.effectHeatCool, a.effectWater, a.effectLighting, a.effectAppliance, a.savings, button_html, 0)
	     
	energy_list = """[ '%s',%f, %f, %f, %f, '%s', "%s",%d],""" % ("No new action",heatCoolMod, waterMod, lightingMod, applianceMod, ' ',' ',1) + energy_list + """[ '%s',%f, %f, %f, %f, '%s', "%s", %d],""" % ("Your baseline",heatCoolMod, waterMod, lightingMod, applianceMod, 'NA','NA',0)

	script_all = script_all + """</script> """
	template_values = {'zipcode':zipcode_value,
			   'city':city,
			   'electricity': electricity,
			   'elecMod': elecMod,
			   'FBid':FBid,
			   'scriptList':script_all,
			   'energyList':energy_list}


	# there are more calculations in the javascript in energy.html
 	# user is shown what is in energy.html
	path = os.path.join(os.path.dirname(__file__), 'energy.html')
        self.response.out.write(template.render(path, template_values))



