#!/usr/bin/python

import urllib2, sys
from BeautifulSoup import BeautifulSoup

def recode(s):
    # udata = s.decode('utf-8', 'ignore')
    return s.encode('ascii', 'xmlcharrefreplace')

#letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#letters.append('0-9')
import urllib2

url = 'http://www.foodinspectionweb.vcha.ca/Facility?search-term=&report-type=ffffffff-ffff-ffff-ffff-fffffffffff1&area=&sort-by=Name&page=0&page-size=9999'

f = urllib2.urlopen(url % i)
buf = f.read()
f.close()
g = open('restaurants.html' % i, 'w')
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
        tdlist.append(tr.a['href'])
        restos.append(tdlist)

print '\n'.join(['\t'.join(resto) for resto in restos])
