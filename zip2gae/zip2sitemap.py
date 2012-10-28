# purpose of this script is to read in the 
# zip code file and then upload a subset to
# google app engine

# need to improve such that it
# 1. reads where it last left off
# 2. writes 2000 of the next lines to the file

import os
import re

#os.system('rm /Users/rwpinder/Projects/next.climate/data/zip_maxtemp.subset.csv')


class zip2sitemap:
    def __init__(self, a):
        v=re.split(',',a)
	self.zipcode = v[0]

	#<?xml version="1.0" encoding="UTF-8"?>
	#<urlset xmlns="http://www.nextclimate.org">

	self.entry = '''
	<url>
	<loc>http://www.nextclimate.org/queryZip/%s/</loc>
	<priority>1.0</priority>
	<changefreq>monthly</changefreq>
	<lastmod>2012-10-22</lastmod>
	</url>
	''' % (v[0])


    def write(self):
	return(self.entry)


i = 0
fin = open('/Users/rwpinder/Projects/next.climate/data/zip_maxtemp.new.csv', 'r')

zipcodes = dict([(z.zipcode,z) for z in map(zip2sitemap,fin.readlines())])

fin.close()

fout = open('/Users/rwpinder/Projects/next.climate/src/gae/nextclimate/static/sitemap.xml', 'w')

fout.write('<?xml version="1.0" encoding="UTF-8"?>')
fout.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for k,z in zipcodes.iteritems():
    fout.write(z.write())

fout.write('</urlset>')

fout.close()

