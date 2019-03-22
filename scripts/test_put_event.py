import urllib2
import sys
opener=urllib2.build_opener(urllib2.HTTPHandler)

while True:
    line = sys.stdin.readline()
    if line == None:
        break
    request=urllib2.Request('http://localhost:8000/put_event',data=line)
    request.get_method=lambda:'PUT'
    url=opener.open(request)
    url.read()
