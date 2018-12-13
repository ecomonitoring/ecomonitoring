import urllib2
import sys
opener=urllib2.build_opener(urllib2.HTTPHandler)

for line in sys.stdin:
    request=urllib2.Request('http://localhost:8000/put_event',data=line)
    request.get_method=lambda:'PUT'
    url=opener.open(request)
    url.read()
