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
                data_processor.put_event(b)
            else:
                raise "error"
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
        except:
            process_error(s)
    
    def do_GET(s):
        try:
            s.serve_static()
        except:
            process_error(s)

    def serve_static(s):
        pass

    def process_error(s):
        info=sys.exc_info()
        traceback.print_exception(*info)
        s.send_response(503)
        s.send_header("Content-type", "text/html")
        s.end_headers()
   
class GraphiteClient():
    def put_event(s, data_lib,config):
        s.sock.sendto("%d:%d|c"%(data_lib['sensor'],data_lib['value']), (config.host,config.graphite_port))

    def __init__(s,config):
        s.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        

class DBClient:
    def put_event(s,data_lib):
        s.cursor.execute("INSERT INTO events(value,sensor) VALUES (%d,%d);"%(data_lib['value'],data_lib['sensor']))

    def __init__(s,config):
        s.cnx = mysql.connector.connect(user=config.user,password=config.password,host=config.host,database=config.database)
        s.cursor =s.cnx.cursor()

    def close(s):
        s.cnx.close()
        s.cursor.close()


class DataProcessor:
    def __init__(s,config,DB,Gl):
    DB(config)
    Gl(config)

    def put_event(s,lib,config):
    DB.put_event(lib)
    Gl.put_event(lib)

    def close(s):
        DB.close


config=Config("config_server.txt")
DB=DBClient 
Gl=GraphiteClient
data_processor=DataProcessor(config,DB,Gl) 


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
print "sucsess"
