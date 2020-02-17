import http.server
import socketserver
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-p', '--port', dest='port', help='specify port number')

PORT = parser.parse_args().port
if os.getcwd() == '/':
    os.chdir('/app')
print('initial port', PORT, os.getcwd())
os.environ['SERVER_PORT'] = PORT
make run-dev PORT=1234

class MyHTTPHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsedURL = urlparse(self.path)
        print(parsedURL)

        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        handler = logging.FileHandler('server.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
        isoDate = datetime.datetime.now().isoformat()
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
            joinedStr = 'Hello '
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

        
        root.info(str.format('{} {} {}', isoDate, str(status), parsedURL.path))
        return

try:
    server = http.server.HTTPServer(('', int(PORT)), MyHTTPHandler)
    print('Started http server on port', PORT)
except KeyboardInterrupt:
    print('^C received, shutting down server')