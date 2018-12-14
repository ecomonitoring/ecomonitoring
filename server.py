import time 
import BaseHTTPServer 
import json 
import traceback 
import sys 
import mysql.connector 
import socket 

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
    def do_PUT (s):
        try:
            """Respond to a PUT request."""

            if s.path=="/put_event":
                len=int(s.headers.getheader('content-length'))
                a=s.rfile.read(len)
                b=json.loads(a)
                event=Event(b,s.client_address[0])
                data_processor.put_event(event)
            else:
                raise "error"
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
        except:
            s.process_error()

    def do_GET(s):
        try:
            s.serve_static()
        except:
            s.process_error()

    def serve_static(s):
        pass

    def process_error(s):
        info=sys.exc_info()
        traceback.print_exception(*info)
        s.send_response(503)
        s.send_header("Content-type", "text/html")
        s.end_headers()

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

    def __init__(s,config):
        s.cnx = mysql.connector.connect(user=config.user,database=config.database,password=config.password,host=config.host)
        s.cursor =s.cnx.cursor()
        s.add_event=("INSERT INTO events (value,sensor,date_time,IP) VALUES (%s,%s,%s,%s)")
        print("DB connectin-OK\n")

    def close(s):
        s.cnx.commit()
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
