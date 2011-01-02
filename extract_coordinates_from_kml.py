#!/usr/bin/python

from BeautifulSoup import BeautifulStoneSoup

f = open('VCH Restaurant Data.kml', 'r')
buf = f.read()
f.close()

soup = BeautifulStoneSoup(buf)
for placemark in soup.findAll('placemark'):
    guid = placemark.find('data', {'name': 'Restaurant GUID'}).value.text
    coordinates = placemark.coordinates.text
    coordinates = ','.join( coordinates.split(',')[:-1] ) # trim the z coordinate
    print '%s\t%s' % (guid, coordinates)

