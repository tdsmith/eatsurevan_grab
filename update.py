#!/usr/bin/python
# update.py
# Updates the eatsure database.

import urllib2, time, sys, os, json, urllib
from BeautifulSoup import BeautifulSoup

url = 'http://www.foodinspectionweb.vcha.ca/Facility?search-term=&report-type=ffffffff-ffff-ffff-ffff-fffffffffff1&area=&sort-by=Name&page=0&page-size=9999'

def recode(s):
    return s.encode('ascii', 'xmlcharrefreplace')

def find_updated_restaurants():
    # grab the current list of restaurants
    f = urllib2.urlopen(url)
    buf = f.read()
    f.close()
    # parse
    soup = BeautifulSoup(buf)
    restos = []
    trlist = soup.table.findAll('tr')
    for tr in trlist:
        tdlist = tr.findAll('td', text=True)
        if tdlist and tr.a:
            tdlist = [recode(i.strip()) for i in tdlist if i.strip()]
            tdlist.append(tr.a['href'].split('/')[-1])
            restos.append(tdlist)
    # now we have the restaurant list in a table
    # the table has, in tab-separated columns:
    # 0: restaurant name
    # 1: unit, street address
    # 2: jurisdiction (not quite city)
    # 3: date of last inspection (DD-Mon-YYYY)
    # 4: Restaurant GUID

    # now, look at our last update and see if anything is newer
    f = open('restos.tab', 'r')
    buf = f.readlines()
    f.close()
    past_restos = [line[:-1].split('\t') for line in buf]
    
    # create dictionaries to make this next step more fun
    rd, past_rd = {}, {}
    for resto in restos:
        try:
            rd[resto[4]] = (time.strptime(resto[3], '%d-%b-%Y'), resto[4])
        except:
            pass # give up if it doesn't have a date
    for resto in past_restos:
        try:
            past_rd[resto[4]] = (time.strptime(resto[3], '%d-%b-%Y'), resto[4])
        except:
            pass

    new_restaurants = [rd[key][1] for key in rd if not (key in past_rd)]
    updated_restaurants = [rd[key][1] for key in rd if (key in past_rd and rd[key][0] > past_rd[key][0])]
    deleted_restaurants = [past_rd[key][1] for key in past_rd if not (key in rd)]
    return restos, new_restaurants, updated_restaurants, deleted_restaurants

def fetch_restos(restos):
    # fetch_restos([resto_guid0, resto_guid1, ...])
    url = 'http://www.foodinspectionweb.vcha.ca/Facility/Show/%s'
    for (i, guid) in enumerate(restos):
        print guid, i, len(restos)
        f = urllib2.urlopen(url % guid)
        buf = f.read()
        f.close()
        g = open('restos/%s.html' % guid, 'w')
        g.write(buf)
        g.close()

def fetch_inspections(inspections):
    # fetch_inspections([inspection_guid0, inspection_guid1, ...])
    url = 'http://www.foodinspectionweb.vcha.ca/Inspection/Show/%s'
    for (i, guid) in enumerate(inspections):
        try:
            print guid, i, len(inspections)
            f = urllib2.urlopen(url % guid)
            buf = f.read()
            f.close()
            g = open('inspections/%s.html' % guid, 'w')
            g.write(buf)
            g.close()
        except:
            print '\tIgnoring exception'

def find_new_inspections(restos):
    # mission_inspection_guids = find_new_inspections([resto_guid0, resto_guid1, ...])
    missing = []
    for resto in restos:
        # load and parse the restaurant page
        f = open('restos/%s.html' % resto)
        buf = f.read()
        f.close()
        soup = BeautifulSoup(buf)
        inspections = []
        try:
            inspP = soup.findAll('table')[1]
            links = inspP.findAll('a')
            for link in links:
                inspDate = link.string
                inspGuid = link['href'].split('/')[-1]
                inspType = link.parent.nextSibling.nextSibling.contents[0].strip()
                inspections.append( (inspGuid, inspDate, inspType) )
        except:
            print '\tIgnoring exception'
        my_missing = []
        for insp in inspections:
            if not os.path.exists('inspections/%s.html' % insp[0]):
                my_missing.append(insp)
        if my_missing:
            missing.append( (resto, my_missing) )
    return missing

def geocode_restos(restos, guidlist):
    # {'guid0': 'lat0,long0', ...} = geocode_restos(restos_table, [guid0, ...])

    google_url = 'http://maps.googleapis.com/maps/api/geocode/json?'
    google_params = [('region', 'ca'), ('language', 'en'), ('sensor', 'false')]

    f = open('jurisdictions.tab', 'r')
    jurisbuf = f.readlines()
    f.close()
    jurisbuf = [line[:-1].split('\t') for line in jurisbuf]
    juris = {}
    for line in jurisbuf:
        juris[line[0]] = line[1]

    # re-parse restos into a lookup table
    resto_d = {}
    for line in restos:
        resto_d[line[4]] = line[:3]

    out = {}

    for guid in guidlist:
        resto = resto_d[guid]
        # skip any entries without an address
        if not resto[1]: continue
        # skip any bogus/non-Vancouver jurisdictions
        bogons = ['Bellas', 'North Shore Residential', 'Water - Misc']
        if resto[2] in bogons: continue
        if 'proposed' in line[0].lower(): continue
        # attempt to normalize the jurisdiction field
        resto[2] = juris[resto[2]]

        address = "%s, %s, BC" % (resto[1], resto[2])
        query_string = urllib.urlencode(google_params + [('address', address)])
        f = urllib2.urlopen(google_url + query_string)
        result = json.load(f)
        f.close()
        ll = result['results'][0]['geometry']['location']
        out[guid] = '%s,%s' % (ll['lat'], ll['lng'])
    return out


def main():
    print 'Fetching restaurant list (this may take a moment)...'
    restos, new_restaurants, updated_restaurants, deleted_restaurants = find_updated_restaurants()
    #f = open('update_state.repr', 'w')
    #print >> f, repr( (restos, new_restaurants, updated_restaurants, deleted_restaurants) )
    #f.close()
    #f = open('update_state.repr')
    #(restos, new_restaurants, updated_restaurants, deleted_restaurants) = eval(f.read())
    #f.close()
    print 'New restaurants'
    print new_restaurants
    print 'Updated restaurants'
    print updated_restaurants
    print 'Deleted restaurants'
    print deleted_restaurants

    print 'Fetching new restaurants...'
    fetch_restos(new_restaurants)

    print 'Fetching updated restaurants...'
    fetch_restos(updated_restaurants)

    print 'Geocoding new restaurants...'
    new_geocoding = geocode_restos(restos, new_restaurants)
    f = open('geocoded_restos.tab', 'a')
    print >> f, '\n'.join(['\t'.join((key, new_geocoding[key])) for key in new_geocoding])
    f.close()

    print 'Writing new restos.tab...'
    f = open('restos.tab', 'w')
    print >> f, '\n'.join(['\t'.join(resto) for resto in restos])
    f.close()

    print 'Identifying new inspections...'
    missing = find_new_inspections(new_restaurants + updated_restaurants)

    print 'Fetching new inspections...'
    # just make a list of inspection guids that need fetching
    missing_guids = []
    for resto in missing:
        missing_guids.extend([insp[0] for insp in resto[1]])
    fetch_inspections(missing_guids)

    # inspections.repr needs to be regenerated afterwards

if __name__ == '__main__':
    main()

