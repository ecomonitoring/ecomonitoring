import json
import random

while True:
	a={}
	a['value']=random.randint(1,5)
	a['sensor']=random.randint(-40,40)
	print(json.dumps(a))
