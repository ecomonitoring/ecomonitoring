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
 

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_PUT (s):
        try:
            """Respond to a PUT request."""

            if s.path=="/put_event":
                len=int(s.headers.getheader('content-length'))
                a=s.rfile.read(len)
                b=json.loads(a)
                data_processor.put_event(Event(b))
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

class GraphiteClient():
    def put_event(s, data_lib):
        s.sock.sendto("%d.1:%d|c"%(data_lib.ip,data_lib.temperature), (config.host,config.graphite_port))
        s.sock.sendto("%d.2:%d|c"%(data_lib.ip,data_lib.pressure), (config.host,config.graphite_port))
        s.sock.sendto("%d.3:%d|c"%(data_lib.ip,data_lib.illumination), (config.host,config.graphite_port))
        s.sock.sendto("%d.4:%d|c"%(data_lib.ip,data_lib.humidity), (config.host,config.graphite_port))
        s.sock.sendto("%d.5:%d|c"%(data_lib.ip,data_lib.noise), (config.host,config.graphite_port))
        s.sock.sendto("%d.6:%d|c"%(data_lib.ip,data_lib.geiger), (config.host,config.graphite_port))
        s.sock.sendto("%d.7:%d|c"%(data_lib.ip,data_lib.gases), (config.host,config.graphite_port))


    def __init__(s,config):
        s.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.config=config

class DBClient:
    def put_event(s,data_lib):
        s.cursor.execute("INSERT INTO events(value,sensor) VALUES (1,%d),(2,%d),(3,%d),(4,%d),(5,%d),(6,%d),(7,%d);"%(data_lib.temperature,data_lib.pressure,data_lib.illumination,data_lib.humidity,data_lib.noise,data_lib.geiger,data_lib.gases)

    def __init__(s,config):
        s.cnx = mysql.connector.connect(user=config.user,password=config.password,host=config.host,database=config.database)
        s.cursor =s.cnx.cursor()

    def close(s):
        s.cnx.close()
        s.cursor.close()

class Event:
    def _init_(s,lib):
        try:
            self.temperature =  lib[1]
            self.humidity = lib[4]
	    self.pressure =  lib[2]
	    self.gases = lib[7]
            self.ip = lib['ip']
	    self.noise = lib[5]
	    self.geiger = lib[6]
	    self.illumination = lib[3]
	except:
	    s.process_error()

class DataProcessor:
    def __init__(s):
        pass

    def put_event(s,lib):
        DB.put_event(lib)
        Gl.put_event(lib)

    def close(s):
        DB.close

global data_processor,DB,Gl

if __name__=="__main__":
    config=Config("config_server.txt")
    DB=DBClient(config)
    Gl=GraphiteClient(config)

    HOST_NAME = config.servername # !!!REMEMBER TO CHANGE THIS!!! 
    PORT_NUMBER =config.port_number# Maybe set this to 9000. 

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
    print "sucsessfull"
