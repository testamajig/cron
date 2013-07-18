#!/usr/bin/python
from pyga.requests import Tracker, Page, Session, Visitor
import random
import time

tracker = Tracker('UA-7848481-1', 'apocalypsebag.com')

quant = random.randint(10, 100)
ips = ['46.21.16.10', '5.83.240.190', '31.6.128.445', '58.99.64.32', '49.128.32.22']

cnt = 1
while cnt < quant:
    ip = ips[random.randint(0, 4)]
    uri = '/'
    #print "page request %d of %d for %s from %s" % (cnt, quant, uri, ip)

    visitor = Visitor()
    visitor.ip_address = ip
    session = Session()
    page = Page(uri)
    tracker.track_pageview(page, session, visitor)

    cnt += 1
    time.sleep(random.randint(4, 10))
