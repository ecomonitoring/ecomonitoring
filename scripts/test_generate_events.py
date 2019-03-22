#!/usr/bin/python -u

import json
import random
import time
import sys

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
        sys.stdout.flush()
        time.sleep(1) #REMEMBER




