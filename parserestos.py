#!/usr/bin/python
#
# Parses restaurant pages from VCH to understand where to look for inspections,
# how many there are to fetch, and what kind they are.
# Depends on restaurant pages having been previously downloaded to restos/.
# Creates inspections.repr.

import os, sys, cPickle
from BeautifulSoup import BeautifulSoup

f = open('restos.tab', 'r')
buf = f.readlines()
f.close()

buf = [line[:-1].split('\t') for line in buf]

restaurants = []

# restaurant = (guid, [(inspGuid, inspDate, inspType), ...])

for line in buf:
    print>>sys.stderr, line[0]
    guid = line[-1].split('/')[-1]
    try:
        f = open('restos/%s.html' % guid)
        resto = f.read()
        f.close()
    except:
        print 'Skipping; no record found'
        continue
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

