#!/usr/bin/python
import sys
import time
import os
import platform 
import subprocess
from socket import socket

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

now = int( time.time() )
logdir = '/home/cron/files-for-graphite'
files = os.listdir(logdir)
lines = []

for f in files:
    f = logdir +'/'+ f
    rows = open(f, 'r').readlines()
    for row in rows:
        lines.append(row.strip())
    os.remove(f)

message = '\n'.join(lines) + '\n' #all lines must end in a newline
#print message
sock.sendall(message)
