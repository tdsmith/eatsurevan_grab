#!/usr/bin/python
#
# fetchandparselist.py -- run me first
# Gets a list of all restaurants from VCH. Includes restaurant name, address,
# date of last inspection, and the URL to the info page, which includes the
# GUID we'll use to refer to it later.
#
# Run as: python fetchandparselist.py
# Additionally creates restaurants.html.

import urllib2, sys
from BeautifulSoup import BeautifulSoup

# we need this because something in the L's is causing trouble
def recode(s):
    return s.encode('ascii', 'xmlcharrefreplace')

import urllib2

# note magic page-size=9999 parameter
url = 'http://www.foodinspectionweb.vcha.ca/Facility?search-term=&report-type=ffffffff-ffff-ffff-ffff-fffffffffff1&area=&sort-by=Name&page=0&page-size=9999'

f = urllib2.urlopen(url)
buf = f.read()
f.close()
g = open('restaurants.html', 'w')
g.write(buf)
g.close()

restos = []

f = open('restaurants.html', 'r')
buf = f.read()
f.close()
soup = BeautifulSoup(buf)
trlist = soup.table.findAll('tr')
for tr in trlist:
    tdlist = tr.findAll('td', text=True)
    if tdlist and tr.a:
        tdlist = [recode(i.strip()) for i in tdlist if i.strip()]
        tdlist.append(tr.a['href'].split('/')[-1])
        restos.append(tdlist)

# tab-separated columns:
# 0: restaurant name
# 1: unit, street address
# 2: jurisdiction (not quite city)
# 3: date of last inspection (DD-Mon-YYYY)
# 4: Restaurant GUID
f = open('restos.tab', 'w')
print >> f, '\n'.join(['\t'.join(resto) for resto in restos])
f.close()
