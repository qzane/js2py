#!/usr/bin/python
# author: qzane
# Native python jsonp server
# Work well with both py2.7 and py3.6
try:
    import http.server as BaseHTTPServer # for py3
except:
    import BaseHTTPServer # for py2
    
import time
import json

HOST_NAME = '0.0.0.0' 
PORT_NUMBER = 18263 # best between 9999 ~ 32768
# you should also implement your own "get_result" function


def get_result(params):
    print('wait some while')
    time.sleep(1) # simulate network delay
    try:
        add1 = int(params['add1'])
    except:
        add1 = 0
    try:
        add2 = int(params['add2'])
    except:
        add2 = 0

    print('add1', add1, 'add2', add2)
    result = {'ans':add1+add2} # this will be encoded as json dictionary and sent back to the browser
    return result


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        print("#%s#"%s.path) # print the incoming request for debugging
        
        try: # get the parameters from the incoming url
            params = {i.split('=')[0]:i.split('=')[1] 
                      for i in s.path.split('?')[-1].split('&')}
        except:
            params = {}     
        
        res = get_result(params)
        
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        
        s.wfile.write("successCallback(".encode('utf-8'))
        s.wfile.write(json.dumps(res).encode('utf-8'))
        s.wfile.write(")".encode('utf-8'))

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    print(r"Try to visit http://127.0.0.1:%s/?add1=123&add2=111" %(PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

