#!/usr/bin/python
import sys
import time
import os
import platform 
import subprocess
from socket import socket
import urllib
import urllib2
import simplejson as json
import math

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

delay = 600
if len(sys.argv) > 1:
  delay = int( sys.argv[1] )

def get_weather_by_city(city):
    params = { 'q': city }
    url = 'http://api.openweathermap.org/data/2.1/find/name?' + urllib.urlencode(params)
    response = json.load(urllib2.urlopen(url))

    #print json.dumps(response, indent=4)

    lines = []

    response = response['list'][0]
    celsius = round(float(response['main']['temp']) - 273.15, 2)
    fahrenheit = round(9.0 / 5.0 * celsius + 32, 2)

    state = city.split(', ')[1].replace(' ', '-').lower()
    city = city.split(', ')[0].replace(' ', '-').lower()
    clouds = response['clouds']['all']
    wind = response['wind']['speed']

    lines.append("weather.%s.%s.temp %s %d" % (state, city, fahrenheit, now))
    lines.append("weather.%s.%s.clouds %s %d" % (state, city, clouds, now))
    lines.append("weather.%s.%s.wind.speed %s %d" % (state, city, wind, now))

    return lines

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)


#while True:
now = int( time.time() )
lines = []

for line in get_weather_by_city('San Francisco, California'):
    lines.append(line)

#for line in get_weather_by_city('Nevada City, California'):
#    lines.append(line)
    #print json.dumps(weather, indent=4)

message = '\n'.join(lines) + '\n' #all lines must end in a newline
#print "sending message\n"
#print '-' * 80
#print message
#print
sock.sendall(message)
#time.sleep(delay)
