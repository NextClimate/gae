from google.appengine.tools import bulkloader
import datetime
from google.appengine.ext import db

# Import the app's data models directly into
# this namespace.  We must add the app
# directory to the path explicitly.
import sys
import os.path
sys.path.append(
    os.path.abspath(
    os.path.dirname(
    os.path.realpath(__file__))))

	#from google.appengine.ext.db import Model
#from models import *


# def get_date_from_str(s):
#     if s:
#         return datetime.datetime.strptime(s, '%m/%d/%Y').date()
#     else:
#         return None



class Zipcode(db.Model):
  """Models an individual zipcode associated with climate change values"""
  zipcode=db.StringProperty()
  city = db.StringProperty(multiline=False)
  state = db.StringProperty(multiline=False)
  maxTobs_1990 = db.IntegerProperty()
  maxTa1_2050 = db.IntegerProperty()
  maxTa1_2090 = db.IntegerProperty()    
  maxTb2_2090 = db.IntegerProperty()


class ZipLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Zipcode',
            [('zipcode', str),
             ('city', str),
             ('state', str),
             ('maxTobs_1990', int),
             ('maxTa1_2050', int),
             ('maxTa1_2090', int),
             ('maxTb2_2090', int),
	    ])

loaders = [ZipLoader]

