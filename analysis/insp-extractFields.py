#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import glob, sys

inspfiles = [glob.glob('../inspections/*html')[0]]

d = {}

for (i, filename) in enumerate(inspfiles):
    print >> sys.stderr, float(i)/len(inspfiles)
    f = open(filename, 'r')
    soup = BeautifulSoup(f.read())
    f.close()

    # inspection date
    inspDate = soup.find('th', text='Inspection Date: ').findNext('td').text
    inspReason = soup.find('th', text='Reason for Inspection: ').findNext('td').text
    print inspDate, inspReason

    # extract the violation headings
    headings = soup.findAll('h4')
    for heading in headings:
        vio = heading.text.strip()
        d[vio] = d.setdefault(vio, 0) + 1
        vioTable = heading.parent.parent.findAll('td')
        obsNew = vioTable[1].text
        obsResolved = vioTable[2].text
        vioText = '\n'.join([i.text for i in heading.findNextSiblings('p')])
        print vio, obsNew, obsResolved, vioText

sortedVios = sorted([(j,i) for (i,j) in d.items()])

print 'Violation\tCount'
for (count, name) in sortedVios:
    print '%s\t%d' % (name, count)

