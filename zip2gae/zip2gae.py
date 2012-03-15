# purpose of this script is to read in the 
# zip code file and then upload a subset to
# google app engine

# need to improve such that it
# 1. reads where it last left off
# 2. writes 2000 of the next lines to the file

import os

#os.system('rm /Users/rwpinder/Projects/next.climate/data/zip_maxtemp.subset.csv')

i = 0
fout = open('/Users/rwpinder/Projects/next.climate/data/zip_maxtemp.subset.csv', 'r')
for line in fout:
    i = i + 1

fout.close()
endline = line
print endline

i = 0
found_end_line = 0

fout = open('/Users/rwpinder/Projects/next.climate/data/zip_maxtemp.subset.csv', 'w')
f =  open('/Users/rwpinder/Projects/next.climate/data/zip_maxtemp.low.csv') 

for line in f:
    if ((found_end_line) and (i<2900)):
	print line
	i = i + 1
	fout.write(line)
    if (line == endline):
	found_end_line = 1

fout.close()
f.close()

os.system('bulkloader.py --application=s~nextclimate --url=http://nextclimate.appspot.com/remote_api --config_file=../gae/nextclimate/loaders.py --kind=Zipcode --filename=../../data/zip_maxtemp.subset.csv')


