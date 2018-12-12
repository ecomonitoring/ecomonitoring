import json
import random

while True:
        a={}
        a['sensor']='temperature'
        a['value']=random.randint(-40,40)
        print(json.dumps(a))
        a['sensor']='pressure'
        a['value']=random.randint(730,760)
        print(json.dumps(a))
        a['sensor']='illumination'
        a['value']=random.randint(-40,40)
        print(json.dumps(a))
        a['sensor']='humidity'
        a['value']=random.randint(-40,40)
        print(json.dumps(a))
        a['sensor']='noise'
        a['value']=random.randint(-40,40)
        print(json.dumps(a))
        a['sensor']='geiger'
        a['value']=random.randint(0,210)
        print(json.dumps(a))
        a['sensor']='gases'
        a['value']=random.randint(-40,40)
        print(json.dumps(a))




