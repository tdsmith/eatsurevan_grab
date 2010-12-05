#!/usr/bin/python

import os, sys, cPickle
from BeautifulSoup import BeautifulSoup

# from restoObjs import Restaurant, Inspection

f = open('restos.tab', 'r')
buf = f.readlines()
f.close()

buf = [line[:-1].split('\t') for line in buf]

restoObjs = []
restaurants = []

# restaurant = (guid, [(inspGuid, inspDate, inspType)]]

for line in buf:
    print>>sys.stderr, line[0]
    guid = line[-1].split('/')[-1]
    f = open('restos/%s.html' % guid)
    resto = f.read()
    f.close()
    soup = BeautifulSoup(resto)
    try:
        inspectionsPara = soup.findAll('table')[1]
        links = inspectionsPara.findAll('a')
        inspections = []
        for link in links:
            inspDate = link.string
            inspGuid = link['href'].split('/')[-1]
            inspType = link.parent.nextSibling.nextSibling.contents[0].strip()
            inspections.append( (inspGuid, inspDate, inspType) )
        restaurants.append( (guid, inspections) )
    except:
        print 'Ignoring exception'

print restaurants

f = open('inspections.repr', 'w')
print >> f, repr(restaurants)
#cPickle.dump(restaurants, f, protocol=-1)
f.close()

