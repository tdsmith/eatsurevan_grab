#!/usr/bin/python

import glob, os
from BeautifulSoup import BeautifulSoup

# repo = {'rguid0': resto0, 'rguid1': resto1}
#
# resto = {'name': 'name',
#          'lat': '-49.1',
#          'long': '123.4',
#          'street': '1234 #3 Road',
#          'jurisdiction': 'Vancouver - North',
#          'update': '25-Aug-2010',
#          'inspections': [inspection0, inspection1, ..., inspectionN]}
#
# inspection = {'date': '27-Feb-2010',
#               'guid': 'guid',
#               'reason': 'Compliance', # or Routine, or Re-inspection
#               'actions': ['action0', 'action1', ...]
#               'findings': [finding0, finding1, ..., findingN]}
#
# finding = ('heading', 'description', numNew, numResolved)

def main():
    # understand the restaurant table
    # 0: restaurant name
    # 1: unit, street address
    # 2: jurisdiction (not quite city)
    # 3: date of last inspection (DD-Mon-YYYY)
    # 4: Restaurant GUID
    f = open('restos.tab', 'r')
    buf = f.readlines()
    f.close()
    restos = [line[:-1].split('\t') for line in buf]

    # load the geocoding data
    f = open('geocoded_restos.tab')
    buf = f.readlines()
    f.close()
    geocodes = dict( [ (resto, latlong.split(',')) for (resto, latlong) in [line[:-1].split('\t') for line in buf if len(line) > 1]] )

    # add restaurants, ignoring ones we don't have geocoding data for
    repo = {}
    for line in restos:
        r = {}
        r['name'], r['street'], r['jurisdiction'], r['update'], rguid = line
        if rguid not in geocodes: continue
        r['lat'], r['long'] = geocodes[rguid]
        r['inspections'] = []
        repo[rguid] = r
    
    # look through our table of inspections and map inspection IDs to restaurant IDs
    f = open('inspections.repr')
    inspections = eval(f.read())
    f.close()
    rID_by_inspection = {}
    for resto in inspections:
        for inspection in resto[1]:
            rID_by_inspection[inspection[0]] = resto[0]

    # now, look over the inspections themselves
    inspfiles = glob.glob('inspections/*html')
    for (i, filename) in enumerate(inspfiles):
        iguid = os.path.basename(filename)[:-5]
        # this is an old inspection file: we don't have a record of it anymore
        # probably, we should delete it.
        if not iguid in rID_by_inspection: continue
        if not rID_by_inspection[iguid] in repo: continue

        inspection = {'guid': iguid}

        print float(i)/len(inspfiles)
        f = open(filename, 'r')
        soup = BeautifulSoup(f.read())
        f.close()

        # inspection date
        inspection['date'] = soup.find('th', text='Inspection Date: ').findNext('td').text
        inspection['reason'] = soup.find('th', text='Reason for Inspection: ').findNext('td').text
        inspection['actions'] = soup.find('th', text='Action Taken: ').findNext('td').text.split(', ')
        inspection['followup'] = soup.find('th', text='Follow-up Required: ').findNext('td').text
        inspection['findings'] = []

        # extract the violation headings
        headings = soup.findAll('h4')
        for heading in headings:
            vio = heading.text.strip()
            vioTable = heading.parent.parent.findAll('td')
            obsNew = vioTable[1].text
            obsResolved = vioTable[2].text
            vioText = '\n'.join([i.text for i in heading.findNextSiblings('p')])
            inspection['findings'].append( (vio, vioText, int(obsNew), int(obsResolved)) )

        repo[rID_by_inspection[inspection['guid']]]['inspections'].append(inspection)

    print 'Writing repository...'
    f = open('repo.repr', 'w')
    print >> f, repr(repo)
    f.close()


if __name__ == '__main__':
    main()

