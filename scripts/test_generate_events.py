import json
import random

while True:
        a={}
        a['value']='temperature'
        a['sensor']=random.randint(-40,40)
        print(json.dumps(a))
        a['value']='pressure'
        a['sensor']=random.randint(730,760)
        print(json.dumps(a))
        a['value']='illumination'
        a['sensor']=random.randint(-40,40)
        print(json.dumps(a))
        a['value']='humidity'
        a['sensor']=random.randint(-40,40)
        print(json.dumps(a))
        a['value']='noise'
        a['sensor']=random.randint(-40,40)
        print(json.dumps(a))
        a['value']='geger'
        a['sensor']=random.randint(0,210)
        print(json.dumps(a))
        a['value']='gases'
        a['sensor']=random.randint(-40,40)
        print(json.dumps(a))




