#!/usr/bin/python
#
# fetchrestos.py
# Invoke after fetchandparselist.py. Actually goes out and grabs all of the
# restaurant HTML files.
# Expects restos/ to exist in the current working directory.
# Depends on restos.tab.

import urllib2, sys

url = 'http://www.foodinspectionweb.vcha.ca/Facility/Show/%s'

f = open('restos.tab', 'r')
buf = f.readlines()
f.close()

buf = [line[:-1].split('\t') for line in buf]

for line in buf:
    print>>sys.stderr, line[0]
    guid = line[-1]
    f = urllib2.urlopen(url % guid)
    buf = f.read()
    f.close()
    g = open('restos/%s.html' % guid, 'w')
    g.write(buf)
    g.close()

