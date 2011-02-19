#!/usr/bin/python
#
# Fetches individual inspection report pages. Expects a directory
# called inspections to exist beneath the current working directory.
# Depends on inspections.repr existing; should have been created by
# (and is described in) parserestos.py.

import urllib2, sys

url = 'http://www.foodinspectionweb.vcha.ca/Inspection/Show/%s'

f = open('inspections.repr', 'r')
buf = f.read()
f.close()
restos = eval(buf)

start, end = int(sys.argv[1]), int(sys.argv[2])

i = 0

for resto in restos[start:end]:
    print >> sys.stderr, resto[0], i
    i += 1
    inspections = resto[1]
    for inspection in inspections[:1]:
        guid = inspection[0]
        try:
            f = urllib2.urlopen(url % guid)
            buf = f.read()
            f.close()
            g = open('inspections/%s.html' % guid, 'w')
            g.write(buf)
            g.close()
        except:
            print >> sys.stderr, '   Ignoring exception'


