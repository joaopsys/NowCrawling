__author__ = 'jota'

import urllib.request
import urllib.parse
import re

keyword = "fall out boy"
types = "(mp3|wma|aac|flac)"
customsearch = "intitle: index of"

query = urllib.parse.urlencode({'num':100,'q': keyword+" "+customsearch+" "+types,"start":0})
url = 'http://google.com/search?%s' % query
print(url)
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent, }

request=urllib.request.Request(url, None, headers)
response = urllib.request.urlopen(request)
data = str(response.read())
p = re.compile('href="\/url\?q=[^\/]*\/\/(?!webcache).*?"')
print('\n'.join(list(x.replace('href="/url?q=', '').replace('"', '') for x in p.findall(data))))

## ToDo FIXME: Check if each page gives 100 results, if not then we've reached the end