# the purpose of this script is to associate
# a zip code with a MSA -- an aggregation of
# zipcodes clustered around a city.
#
# this reads in a comma delimited file
# of zip codes -> states
#    zip codes -> metro area assignments
#    metro codes -> name of area


import re


# step 1, remove duplicates from zipcode -> MSA mapping

fMSA = open('/Users/rwpinder/Projects/next.climate/data/zipcode_MSA_numbers.csv','r')
fout = open('/Users/rwpinder/Projects/next.climate/data/zipcode_MSA_numbers.no_duplicates.csv','w')

last_zip = "0"
for aline in fMSA:
    b = re.split(',',aline,maxsplit=2)
    zip = b[0]
    if (zip != last_zip):
	fout.write(aline)
    last_zip = zip

fout.close()
fMSA.close()


# step 2, add specificity of sub-MSA for large population areas

fout = open('/Users/rwpinder/Projects/next.climate/data/zipcode_MSA_numbers.subMSA.txt','w')


fMSA = open('/Users/rwpinder/Projects/next.climate/data/zipcode_MSA_numbers.no_duplicates.csv','r')

# iterate over each zip code in the MSA file
for aline in fMSA:

    # if there is no sub-MSA, then default to current line
    writeLine = aline
    b = re.split(',',aline, maxsplit=3)

    # iterate over all counties to see if this zip code should
    # be part of a sub-MSA. 
    f = open('/Users/rwpinder/Projects/next.climate/data/zcta_county.txt','r')
    for a2 in f:
	b2 = re.split(',',a2)
	state = b2[1]
	county = b2[2]

	# if zip in MSA file matches zip in county / state file
	# check to see if a sub-MSA should be added
	if (b2[0] == b[0]):
	    # orange county, CA
	    if ((state == "06") and (county == "059")):
		writeLine = b[0]+','+b[1]+',42044,'+b[3] 

	    # west palm beach
	    if ((state == "12") and (county == "099")):
		writeLine = b[0]+','+b[1]+',48424,'+b[3]
	
	    # ft. lauderdale
	    if ((state == "12") and (county == "011")):
		writeLine = b[0]+','+b[1]+',22744,'+b[3] 
	
	    # east bay
	    if (((state == "06") and (county == "001")) or
		((state == "06") and (county == "013"))):
		writeLine = b[0]+','+b[1]+',36084,'+b[3] 
    
	    # DC maryland suburbs
	    if (((state == "24") and (county == "031")) or
		((state == "24") and (county == "021"))):
		writeLine = b[0]+','+b[1]+',13644,'+b[3] 

	    # add addtional sub-MSA's here

	    # sub-MSA added as thrid element in file; exit for loop.
	    break

    fout.write(writeLine)
    
    f.close()

fMSA.close()
fout.close()

# step 3 zip2MSA.py
