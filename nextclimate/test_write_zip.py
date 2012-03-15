#/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/google/appengine/ext/
from google.appengine.ext import db

class Zipcode(db.Model):
  """Models an individual zipcode associated with climate change values"""
  zipcode=db.IntegerProperty()
  city = db.StringProperty(multiline=False)
  state = db.StringProperty(multiline=False)
  maxTobs_1950 = db.IntegerProperty()
  maxTobs_1990 = db.IntegerProperty()
  maxTa1_2050 = db.IntegerProperty()
  maxTa1_2090 = db.IntegerProperty()    
  maxTb2_2090 = db.IntegerProperty()

z1 = Zipcode(zipcode = 27510,
	     city = 'Carrboro',
	     state = 'NC',
	     maxTobs_1950 = 7,
	     maxTobs_1990 = 10,
	     maxTa1_2050 = 20,
	     maxTa1_2090 = 100,
	     maxTb2_2090 = 20)
z1.put()
