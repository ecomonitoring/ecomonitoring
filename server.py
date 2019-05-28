# -*- encoding: utf-8 -*-
import time
import BaseHTTPServer
import json
import traceback
import sys
import mysql.connector
import socket
import risk as myModule

class Config():
    def __init__(self, fname):
        file=open(fname,'r')
        content=file.read()
        settings=json.loads(content)
        self.servername = settings['servername']
        self.port_number=settings['port_number']
        self.host=settings['host']
        self.user=settings['user']
        self.password=settings['password']
        self.database=settings['database']
        self.graphite_port=settings['graphite_port']
        print "Config was read\n"

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def send_answer(s, data, eid):
        cnx = mysql.connector.connect(user=config.user,database=config.database,password=config.password,host=config.host)
        cursor = cnx.cursor()
        cursor.execute("select value from limits where id =" + eid + ";")

        for (value) in cursor:
            data["norm_conc"] = value
            #print value

        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        #print json.dumps(data)
        s.wfile.write(json.dumps(data))

        cursor.close()
        cnx.close()

    def do_PUT (s):
        try:
            """Respond to a PUT request."""

            if s.path == "/put_event":
                len = int(s.headers.getheader('content-length'))
                a = s.rfile.read(len)
                b = json.loads(a)
                event = Event(b,s.client_address[0])
                data_processor.put_event(event)
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()


            elif s.path == "/add_data/1_1":
                len = int(s.headers.getheader('content-length'))
                a = s.rfile.read(len)
                data = json.loads(a)
                DB.risc1_1(data['elem_id'], data['concentration'], data['et_child'], data['et_adult'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r = counter(1, 1, data['concentration'], data['et_child'], data['et_adult'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r['pid'] = "div1_1"
                s.send_answer(r, data['elem_id'])

            elif s.path=="/add_data/1_2":
                len = int(s.headers.getheader('content-length'))
                a = s.rfile.read(len)
                data = json.loads(a)
                DB.risc1_2(data['elem_id'], data['concentration'], data['ir_child'], data['ir_adult'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r = counter(1, 2, data['concentration'], data['ir_child'], data['ir_adult'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r['pid'] = "div1_2"
                s.send_answer(r, data['elem_id'])

            elif s.path=="/add_data/2_1":
                len = int(s.headers.getheader('content-length'))
                a = s.rfile.read(len)
                data = json.loads(a)
                DB.risc2_1(data['elem_id'], data['concentration'], data['et_child'], data['et_adult'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r = counter(2, 1, data['concentration'], data['et_child'], data['et_adult'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r['pid'] = "div2_1"
                s.send_answer(r, data['elem_id'])

            elif s.path=="/add_data/2_2":
                len = int(s.headers.getheader('content-length'))
                a = s.rfile.read(len)
                data = json.loads(a)
                DB.risc2_2(data['elem_id'], data['concentration'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r = counter(2, 2, data['concentration'], 0, 0, data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r['pid'] = "div2_2"
                s.send_answer(r, data["elem_id"])

            elif s.path=="/add_data/3_1":
                len = int(s.headers.getheader('content-length'))
                a = s.rfile.read(len)
                data = json.loads(a)
                DB.risc3_1(data['elem_id'], data['concentration'], data['et_child'], data['et_adult'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r = counter(3, 1, data['concentration'], data['et_child'], data['et_adult'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r['pid'] = "div3_1"
                s.send_answer(r, data['elem_id'])

            elif s.path=="/add_data/3_2":
                len = int(s.headers.getheader('content-length'))
                a = s.rfile.read(len)
                data = json.loads(a)
                DB.risc3_2(data['elem_id'], data['concentration'], data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r = counter(1, 1, data['concentration'], 0, 0, data['ef_child'], data['ef_adult'], data['ed'], data['popl_child'], data['popl_adult'])
                r['pid'] = "div3_2"
                s.send_answer(r, data["elem_id"])

            else:
                raise "error"
        except:
            s.process_error()

    def do_GET(s):
        if s.path == "/get_risk":
            s.send_answer()
        
        fname = s.path.split('/')[-1]
        with open(fname, "r") as file:
            s.send_response(200)
            if fname.endswith(".html"):
                s.send_header("Content-type", "text/html")

            elif fname.endswith(".js"):
                s.send_header("Content-type", "text/javascript")

            elif fname.endswith(".css"):
                s.send_header("Content-type", "text/css")
            else:
                s.send_header("Content-type", "text/php")
            s.end_headers()
            s.wfile.write(file.read())

    def do_POST(s):
        l=int(s.headers.getheader('content-length'))
        content=s.rfile.read(l)
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write(content)


    def serve_static(s):
        pass

    def process_error(s):
        info=sys.exc_info()
        traceback.print_exception(*info)
        s.send_response(503)
        s.send_header("Content-type", "text/html")
        s.end_headers()

def counter(a, b, concentration, et_child, et_adult, ef_child, ef_adult, ed, popl_child, popl_adult):
        q = myModule.risk();
        risk = myModule.Count(a, b, float(concentration), float(et_child), float(et_adult), float(ef_child), float(ef_adult), float(ed), float(popl_child), float(popl_adult), q)
        return risk;


class GraphiteClient:
    def put_event(s, event):
        sensor_string="events.%s.%s:%d|c"%(event.ip.replace(".", "_"),event.name,event.value)
        print sensor_string
        s.sock.sendto(sensor_string, (config.host,config.graphite_port))
    def __init__(s,conf):
        s.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.config=conf
        print("Graphite connection- OK\n")

class DBClient:
    def put_event(s,event):
        s.cursor.execute(s.add_event,event.event_data)
        s.cnx.commit()

    def risc1_1(s, id, conc, ChTm, AdTm, ChCa, AdCa, Dur, ChCo, AdCo):
        add_1_1=("INSERT INTO Underground_water_skin (Elem_ID, Concentration, Child_Time, Adult_Time, Child_Cases, Adult_Cases, Duration, Child_Count, Adult_Count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        s.cursor.execute(add_1_1, (id, conc, ChTm, AdTm, ChCa, AdCa, Dur, ChCo, AdCo))
        s.cnx.commit()

    def risc1_2(s, id, conc, ChTm, AdTm, ChCa, AdCa, Dur, ChCo, AdCo):
        add_1_2=("INSERT INTO Underground_water_peros (Elem_ID, Concetration, Child_Time, Adult_Time, Child_Cases, Adult_Cases, Duration, Child_Count, Adult_Count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        s.cursor.execute(add_1_2, (id, conc, ChTm, AdTm, ChCa, AdCa, Dur, ChCo, AdCo))
        s.cnx.commit()

    def risc2_1(s, id, conc, ChTm, AdTm, ChCa, AdCa, Dur, ChCo, AdCo):
        add_2_1=("INSERT INTO Surface_water_skin (Elem_ID, Concentration, Child_Time, Adult_Time, Child_Cases, Adult_Cases, Duration, Child_Count, Adult_Count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        s.cursor.execute(add_2_1, (id, conc, ChTm, AdTm, ChCa, AdCa, Dur, ChCo, AdCo))
        s.cnx.commit()

    def risc2_2(s, id, conc, ChCa, AdCa, Dur, ChCo, AdCo):
        add_2_2=("INSERT INTO Surface_water_peros (Elem_ID, Concentration, Child_Cases, Adult_Cases, Duration, Child_Count, Adult_Count) VALUES (%s,%s,%s,%s,%s,%s,%s)")
        s.cursor.execute(add_2_2, (id, conc, ChCa, AdCa, Dur, ChCo, AdCo))
        s.cnx.commit()

    def risc3_1(s, id, conc, ChTm, AdTm, ChCa, AdCa, Dur, ChCo, AdCo):
        add_3_1=("INSERT INTO Ground_skin (Elem_ID, Concentration, Child_Time, Adult_Time, Child_Cases, Adult_Cases, Duration, Child_Count, Adult_Count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        s.cursor.execute(add_3_1, (id, conc, ChTm, AdTm, ChCa, AdCa, Dur, ChCo, AdCo))
        s.cnx.commit()

    def risc3_2(s, id, conc, ChCa, AdCa, Dur, ChCo, AdCo):
        add_3_2=("INSERT INTO Ground_peros (Elem_ID, Concentration, Child_Cases, Adult_Cases, Duration, Child_Count, Adult_Count) VALUES (%s,%s,%s,%s,%s,%s,%s)")
        s.cursor.execute(add_3_2, (id, conc, ChCa, AdCa, Dur, ChCo, AdCo))
        s.cnx.commit()

    def __init__(s,config):
        s.cnx = mysql.connector.connect(user=config.user,database=config.database,password=config.password,host=config.host)
        s.cursor =s.cnx.cursor()
        s.add_event=("INSERT INTO events (value,sensor,date_time,IP) VALUES (%s,%s,%s,%s)")
        print("DB connectin-OK\n")

    def close(s):
        #s.cnx.commit()
        s.cnx.close()
        s.cursor.close()
        print ("DB closed\n")

class Event:
    def __init__(s,lib,IP):
        s.ip = IP
        s.name = lib["sensor"]
        s.value = lib["value"]
        s.sensors = {'temperature':1,'pressure':2,'illumination':3,'humidity':4,'noise':5,'geiger':6,'gases':7}
        s.timestamp=time.asctime()
        s.event_data=(s.value,s.sensors[s.name],s.timestamp,s.ip)

class DataProcessor:
    def __init__(s):
        pass

    def put_event(s,lib):
        DB.put_event(lib)
        Gl.put_event(lib)

    def close(s):
        DB.close()

global data_processor,DB,Gl,event

if __name__=="__main__":
    config=Config("config_server.json")

    DB=DBClient(config)
    Gl=GraphiteClient(config)
    data_processor=DataProcessor()
    HOST_NAME = config.servername
    PORT_NUMBER =config.port_number
    
    server_class=BaseHTTPServer.HTTPServer 
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler) 
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER) 
    try:
        httpd.serve_forever() 
    except KeyboardInterrupt:
        pass 
    httpd.server_close() 
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER) 

    data_processor.close()
    print "sucsessfull\n"
