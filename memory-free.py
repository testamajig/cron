#!/usr/bin/python
"""Copyright 2008 Orbitz WorldWide

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import sys
import time
import os
import platform 
import subprocess
from socket import socket

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

delay = 60 
if len(sys.argv) > 1:
  delay = int( sys.argv[1] )

def get_memfree():
  # For more details, "man proc" and "man uptime"  
    if platform.system() == "Linux":
        free = subprocess.Popen(["free", "-m"], stdout=subprocess.PIPE).communicate()[0]
        free = free.strip().split('\n')
        foo = 0
        for a in free:
            b = a.split()
            if b[0].startswith('-'):
                foo = b[3]
                return foo

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

#while True:
now = int( time.time() )
lines = []
#We're gonna report all three loadavg values
memfree = get_memfree()
lines.append("servers.i-ea6ab8b1.memfree %s %d" % (memfree,now))
message = '\n'.join(lines) + '\n' #all lines must end in a newline
#print "sending message\n"
#print '-' * 80
#print message
#print
sock.sendall(message)
#time.sleep(delay)
