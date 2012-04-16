# the purpose of this script is to associate
# a zip code with a MSA -- an aggregation of
# zipcodes clustered around a city.
#
# this reads in a comma delimited file
# of zip codes -> states
#    zip codes -> metro area assignments
#    metro codes -> name of area


import re

# helper function to remove zip quotes
def noquote(x): return re.sub('\"',"",x) # remove quotes



# class to hold and read in zip codes and MSAs from csv file

class zip2MSA:
    def __init__(self, a):
        v=map(noquote, re.split(',',a))
	
        self.code = v[0]
        self.MSA = v[1]
	subMSA = v[2]
	self.MSAname = "none"
	self.MSAstate = "none"
	
	# iterate over all names in the file to find
	# if there is a name for this MSA
	f = open('/Users/rwpinder/Projects/next.climate/data/MSA_population.txt', 'r')
	# skip header
	for i in range(1,10):
	    f.readline()
	    
	for i in range(1,396):
	    aline = f.readline()
	    #	    print(aline)
	    b = re.split('\"',aline)
	    pattern = re.compile("[A-Z]{2}")
	    popS = re.split(',',b[9])

	    if (len(popS) > 2):
	    	population = 1000000
	    else:
	    	population = int(popS[0]+popS[1])

	    # does this MSA match and is it a metro area with population > 200K?


	    if (subMSA != '1'):
		if ((b[0][0:5] == self.MSA) and (len(b[0]) > 10) and
		    (b[0][6:11] == subMSA) and
		    (population > 200000)):
		    self.MSAname = re.sub('\.',"",re.split(',',b[1])[0])
		    self.MSAstate = pattern.findall(b[1])[0]
		    print(self.code + ' ' + self.MSAname + ', ' + self.MSAstate)
	    else:
		if ((b[0][0:5] == self.MSA) and
		    (b[1][0] != ".") and
		    (population > 200000)):
		    self.MSAname = re.split(',|-',b[1])[0]
		    self.MSAstate = pattern.findall(b[1])[0]
		    print(self.code + ' ' + self.MSAname + ', ' + self.MSAstate)
		
	f.close()

    def write(self):
        return (self.code + ',' + 
		self.MSA + ',' + 
                self.MSAname + ', ' +
     	        self.MSAstate + '\n') 

f = open('/Users/rwpinder/Projects/next.climate/data/zipcode_MSA_numbers.subMSA.txt','r')
#f = open('/Users/rwpinder/Projects/next.climate/data/zp.test.txt','r')    
zipcodes = dict([(z.code,z) for z in map(zip2MSA,f.readlines())])
f.close()

fout = open('/Users/rwpinder/Projects/next.climate/data/zipcode_MSA_names.csv','w')
for k,z in zipcodes.iteritems():
    fout.write(z.write())

fout.close()


