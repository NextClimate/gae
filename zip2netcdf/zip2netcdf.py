# purpose of this script is to read in the 
# zip code file and then perform a function on 
# the netcdf files for each grid cell that falls 
# in that netcdf file location

## define a class for storing zip codes
from scipy.io import netcdf
import re

def noquote(x): return re.sub('\"',"",x) # remove quotes
class zipfree:
    def __init__(self, a):
        v=map(noquote, re.split(',',a))
        self.code = v[0]
        self.type = v[1]
        self.city = v[2]
        self.state = v[3]
        self.primary = v[4]

        if (len(v[5]) > 0): 
            self.lat = float(v[5])
        else:
            self.lat = 0.0
        if (len(v[6]) > 0): 
            self.lon = float(v[6])
        else:
            self.lon = 0.0


f = open('/Users/rwpinder/Projects/next.climate/data/free-zipcode-database-Primary.csv', 'r')
freezips = dict([(z.code,z) for z in map(zipfree,f.readlines())])
f.close()
def matchzip(z,fzs):
    print z
    for k,v in fzs.iteritems():
	if v.code == z:
	    return v




class zip:
    def __init__(self, a):
        v=map(noquote, re.split(',',a))
        self.code = v[0]

        if (len(v[1]) > 0): 
            self.lat = float(v[1])
        else:
            b = matchzip(v[0],freezips)
	    self.lat = b.lat
        if (len(v[2]) > 0): 
            self.lon = float(v[2])
        else:
            b = matchzip(v[0],freezips)
	    self.lon = b.lon

        self.city = v[3]
        self.state = v[4]
        self.county = v[5]
        self.type = v[6]
        self.t50 = 0
        self.t90 = 0
        self.tHope = 0
	self.tobs50 = 0
	self.tobs90 = 0

    def write_zip(self):
        return (self.code + ',' + 
		str(self.lat) + ',' + 
		str(self.lon) + ',' + 
                self.city + ',' + 
                self.state + ',' + 
                self.county + ',' + 
		self.type + '\n')


    def write(self):
        return (self.code + ',' + 
		# str(self.lat) + ',' + 
		# str(self.lon) + ',' + 
                self.city + ',' + 
                self.state + ',' + 
                # self.county + ',' + 
		# self.type + ',' + 
                str(self.tobs5090) + ',' + 
                str(self.t50) + ',' + 
                str(self.t90) + ',' + 
                str(self.tHope) + '\n')



## open text file that includes zip codes
## and build a dictionary of zip code locations
#f = open('/Users/rwpinder/Projects/next.climate/data/zip_codes.subset.csv', 'r')
f = open('/Users/rwpinder/Projects/next.climate/data/zip_codes.csv', 'r')
zipcodes = dict([(z.code,z) for z in map(zip,f.readlines())])
f.close()
## open netcdf file

#file = netcdf.NetCDFFile("/Users/rwpinder/Projects/next.climate/data/"+
#    "/gfdl_cm2_1.noleap.sresb1.run1.tasmax.BCCA_0.125deg.2099.nc","r")
#file.variables.keys()
#t = file.variables['tasmax']


## calculate frequency of days > T degrees F

def daysAboveT(fileName, startYear, endYear, T):
    import numpy as np

    def f(x): return ((x<1e20) and (x>T))

    file = netcdf.NetCDFFile(fileName+str(startYear)+".nc","r")
    t = file.variables['tasmax']
    t50 = np.zeros([endYear-startYear,t.shape[1],t.shape[2]])
    tReturn = np.zeros([t.shape[1],t.shape[2]])

    for year in range(startYear,endYear):
        file = netcdf.NetCDFFile(fileName+str(year)+".nc","r")
        t = file.variables['tasmax']
        for x in range(t.shape[1]):
            print year,x
            for y in range(t.shape[2]):
                t50[year-startYear,x,y] = len(filter(f, t[:,x,y] * 9.0 / 5.0 + 32))
        file.close()

    for x in range(t.shape[1]):
        print year,x
        for y in range(t.shape[2]):
            a = t50[:,x,y]
            a.sort
            tReturn[x,y] = a[int(round(len(a)/2))]

    return tReturn


## from 2046 -- 2065, calculate frequency of days > 90 F
t50 = daysAboveT("/Users/rwpinder/Projects/next.climate/data/"+
                 "gfdl_cm2_1.noleap.sresa2.run1.tasmax.BCCA_0.125deg.",
                 2046,2065,T=90)

    #f_t50 = open("/Users/rwpinder/Projects/next.climate/data/t50.pickle","w")
    #pickle.dump(t50,f_t50)
    #f_t50.close()


## from 2079 -- 2099, calculate frequency of days > 90 F
t90 =  daysAboveT("/Users/rwpinder/Projects/next.climate/data/"+
                 "gfdl_cm2_1.noleap.sresa2.run1.tasmax.BCCA_0.125deg.",
                 2081,2099,T=90)

    #f_t90 = open("/Users/rwpinder/Projects/next.climate/data/t90.pickle","w")
    #pickle.dump(t90,f_t90)
    #f_t90.close()


# repeat for the b2 scenario that represents improved climate
tHope = daysAboveT("/Users/rwpinder/Projects/next.climate/data/"+
		   "gfdl_cm2_1.noleap.sresb1.run1.tasmax.BCCA_0.125deg.",
                   2081,2099,T=90)

    #f_tHope = open("/Users/rwpinder/Projects/next.climate/data/tHope.pickle","w")
    #pickle.dump(tHope,f_tHope)
    #f_tHope.close()

# repeat for the observations 1950 -- 1959
tobs5090 = daysAboveT("/Users/rwpinder/Projects/next.climate/data/"+
		   "gridded_obs.tasmax.OBS_125deg.daily.",
                   1950,1999,T=90)

    #f_tobs5090 = open("/Users/rwpinder/Projects/next.climate/data/tobs5090.pickle","w")
    #pickle.dump(tobs5090,f_tobs5090)
    #f_tobs5090.close()

# to reload
#f_tobs5090 = open("/Users/rwpinder/Projects/next.climate/data/tobs5090.pickle","r")
#b = pickle.load(f_tobs5090)
#f_tobs5090.close()

## iterate through zip codes and assign value for frequency days > 90 F
filename = ("/Users/rwpinder/Projects/next.climate/data/" +
            "/gfdl_cm2_1.noleap.sresb1.run1.tasmax.BCCA_0.125deg.2099.nc")

def getloc(lat, lon, t, filename):
    file = netcdf.NetCDFFile(filename,"r")
    latb = file.variables['lat_bnds']
    lonb = file.variables['lon_bnds']

    if ((lat < min(latb[:,0])) or (lat > max(latb[:,1]))):
	return None

    if ((lon < min(lonb[:,0])) or (lon > max(lonb[:,1]))):
	return None
	
    for i in range(len(latb[:,1])):
	if ((lat > latb[i,0]) and (lat < latb[i,1])): break

    for j in range(len(lonb[:,1])):
	if ((lon > lonb[j,0]) and (lon < lonb[j,1])): break

    a = [t[i,j]]

    for i2 in range(max(0,i-1),min(i+2,len(latb[:,1]))):
	for j2 in range(max(0,j-1),min(j+2,len(lonb[:,1]))):
	    a.append(t[i2,j2])

    def mean(x): return sum(x)/len(x)
    def fzero(x): return x != 0
    a = filter(fzero,a)
    if len(a):
	return int(round(mean(a)))
    else:
	return 0
    

def in_domain(lat, lon, filename):
    file = netcdf.NetCDFFile(filename,"r")
    latb = file.variables['lat_bnds']
    lonb = file.variables['lon_bnds']

    if ((lat < min(latb[:,0])) or (lat > max(latb[:,1]))):
	return False

    if ((lon < min(lonb[:,0])) or (lon > max(lonb[:,1]))):
	return False

    return True



## write output
## need to check here for an easy way to upload to google app engine
fout = open('/Users/rwpinder/Projects/next.climate/data/zip_maxtemp.low.csv','w')
    
for k,v in zipcodes.iteritems():
    print k
    v.tobs5090 = getloc(v.lat, v.lon, tobs5090, filename)
    v.t50 = getloc(v.lat, v.lon, t50, filename)
    v.t90 = getloc(v.lat, v.lon, t90, filename)    
    v.tHope = getloc(v.lat, v.lon, tHope, filename)
    
# do another pass though, this time matching to nearest climate
# during the present time    
#for k,v in zipcodes.iteritems():

# for valid entries, print it out
for k,v in zipcodes.iteritems():
    print k, v.tobs5090, v.t50, v.t90, v.tHope
    if (not(v.tobs5090 and v.t50 and v.t90 and v.tHope)):
	if (in_domain(v.lat, v.lon, filename)):
	    fout.write(v.write())

fout.close()


# for i in range(1,190):
#     print i, matchtemp(i,zipcodes)
    
# def matchtemp(t,fzs):
#     for k,v in fzs.iteritems():
# 	if v.tobs5090 == t:
# 	    return (v.city, v.state)
