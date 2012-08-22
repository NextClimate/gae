
import urllib
import urllib2
import cookielib

url = 'http://solar-estimate.org/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }


urlopen = urllib2.urlopen
Request = urllib2.Request
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

req = Request(url, {}, headers)

handle = urlopen(req)

for index, cookie in enumerate(cj):
    print index, '  :  ', cookie


url = 'http://solar-estimate.org/index.php'

values = {'page' : 'findacontractor',
	  'subpage' : 'show',
	  'from' : 'step2',
	  'state' : '',
	  'county' : '',
	  'zipcode' : '27510',
	  'wantsolar' : '1',
	  # 'wantwater' : '0',
	  # 'wantpool' : '0',
	  # 'wantair' : '0',
	  # 'wantgeo' : '0',
	  # 'wantwind' : '0',
	  # 'wantwood' : '0',	  
	  # 'wantdesign' : '0',
	  # 'wantcooker' : '0',
	  # 'wantpump' : '0',
	  # 'wantengineering' : '0',
	  # 'wantenergyaudit' : '0',
	  # 'wantweatherization' : '0',
	  # 'wantfinance' : '0',
	  'business' : '0'}



data = urllib.urlencode(values)

req = Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()
#print(the_page)
siteNames = re.findall('<span style="font-size:14px;font-weight:bold;text-decoration:underline; color:##00003F;">?(.*?)</span>', the_page)
websites = re.findall('Website: <a href="?(.*?)"? target=_blank>', the_page)

for s, w in zip(siteNames, websites):
    print '<li><a href="%s"> %s </a></li>' % (w,s)


