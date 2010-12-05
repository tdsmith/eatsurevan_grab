#!/usr/bin/python

import cPickle, urllib2, os, sys

url = 'http://www.foodinspectionweb.vcha.ca/Inspection/Show/%s'

f = open('inspections.pickle', 'r')
restos = cPickle.load(f)
f.close()

start, end = int(sys.argv[1]), int(sys.argv[2])

for resto in restos[start:end]:
    print >> sys.stderr, resto[0]
    inspections = resto[1]
    for inspection in inspections[:1]:
        guid = inspection[0]
        f = urllib2.urlopen(url % guid)
        buf = f.read()
        f.close()
        g = open('inspections/%s.html' % guid, 'w')
        g.write()
        g.close()

