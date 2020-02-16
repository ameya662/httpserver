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