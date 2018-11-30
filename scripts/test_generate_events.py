import json
import random

while True:
	a={}
	a['value']=random.randint(1,1000)
	a['temperature']=random.randint(-40,40)
	a['humidity']=random.randint(1,100)
	a['something']=random.randint(-50,50)
	print(json.dumps(a))