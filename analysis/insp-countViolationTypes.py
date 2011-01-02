#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import glob, sys

inspfiles = glob.glob('../inspections/*html')

d = {}

for (i, filename) in enumerate(inspfiles):
    print >> sys.stderr, float(i)/len(inspfiles)
    f = open(filename, 'r')
    soup = BeautifulSoup(f.read())
    f.close()

    # extract the violation headings
    headings = soup.findAll('h4')
    for heading in headings:
        vio = heading.text.strip()
        d[vio] = d.setdefault(vio, 0) + 1

sortedVios = sorted([(j,i) for (i,j) in d.items()])

print 'Violation\tCount'
for (count, name) in sortedVios:
    print '%s\t%d' % (name, count)

