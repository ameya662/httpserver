import http.server
import socketserver
import os
import re
import json
import subprocess
import logging
import sys
import datetime
from argparse import ArgumentParser
from urllib.parse import urlparse

parser = ArgumentParser()
# define command line argument
parser.add_argument('-p', '--port', dest='port', help='specify port number')

# read the arguments from the commandline
PORT = parser.parse_args().port
if os.getcwd() == '/':
    os.chdir('/app')
print('initial port', PORT, os.getcwd())
os.environ['SERVER_PORT'] = PORT

class MyHTTPHandler(http.server.BaseHTTPRequestHandler):
    # handling get requests
    def do_GET(self):
        # parse url into an object
        parsedURL = urlparse(self.path)
        print(parsedURL)
        # create a logger
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        # logger outputs to server.log file
        handler = logging.FileHandler('server.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
        isoDate = datetime.datetime.now().isoformat()
        # default status code is 404 if none of the paths are matching
        status = 404
        if self.path.endswith('favicon.ico'):
            return
        if self.path == '/':
            status = 200
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><head></head><body><p>This server handles 3 endpoints</p>")
            self.wfile.write(b"</body></html>")
        elif parsedURL.path == '/helloworld' and not parsedURL.query == '':
            status = 200
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # split the query string at every capital letter
            matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', parsedURL.query.split(sep='=')[1])
            joinedStr = 'Hello '
            arr = [m.group(0) for m in matches]
            # add a white space between every word
            strWithSpaces = ' '.join(arr)
            result = str.format('<html><head></head><body><p>Hello {}</p>', strWithSpaces)
            self.wfile.write(bytes(result, 'utf-8'))
            self.wfile.write(b"</body></html>")
        elif parsedURL.path == '/helloworld':
            status = 200
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><head></head><body><p>Hello Stranger</p>")
            self.wfile.write(b"</body></html>")
        elif parsedURL.path == '/versionz':
            status = 200
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # get the git hash and git project name
            gitHash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip('\n')
            projectName = str(subprocess.check_output(['git', 'config', 'remote.origin.url'])).split(sep='/')[-1].split('.')[0]
            self.wfile.write(json.dumps({'git_hash': gitHash, 'project_name': projectName}).encode('utf-8'))
        
        root.info(str.format('{} {} {}', isoDate, str(status), parsedURL.path))
        return

try:
    # start the http server listening on the specified port
    server = http.server.HTTPServer(('', int(PORT)), MyHTTPHandler)
    print('Started http server on port', PORT)
    server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    # closes the socket after shutting down the server
    server.socket.close()


    
    
