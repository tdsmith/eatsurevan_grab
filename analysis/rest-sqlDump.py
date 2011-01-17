#!/usr/bin/python

from eatsureutils import sqlDate
import codecs

def sqldump(tlist):
    print """/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` (`restaurant_id`,`location`,`address`,`city`,`latitude`,`longitude`,`inspected`,`critical`,`noncritical`,`updated`,`active`,`closed`,`closed_date`) VALUES """
    # print sql
    ts = [repr(row) for row in tlist] #stringify
    tstrs = ',\n'.join(ts)
    tstrs = tstrs.replace('None', 'NULL')
    print tstrs, ';'
    print '/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;'

def main():
    # get ready to normalize the addresses
    f = open('../jurisdictions.tab', 'r')
    jurisbuf = f.readlines()
    f.close()
    jurisbuf = [line[:-1].split('\t') for line in jurisbuf]
    juris = {}
    for line in jurisbuf:
        juris[line[0]] = line[1]

    # open restos
    # 0: restaurant name
    # 1: unit, street address
    # 2: jurisdiction (not quite city)
    # 3: date of last inspection (DD-Mon-YYYY)
    # 4: Restaurant GUID
    f = open('../restos.tab')
    buf = f.readlines()
    f.close()
    restos = [line[:-1].split('\t') for line in buf]

    # actually normalize
    for line in restos:
        if line[2] in juris: line[2] = juris[line[2]]

    # open our geocode data
    f = open('../geocoded_restos.tab')
    buf = f.readlines()
    f.close()
    geocodes = dict( [ (resto, latlong.split(',')) for (resto, latlong) in [line[:-1].split('\t') for line in buf if len(line) > 1]] )

    # load inspection data so we can get violation counts
    # or not

    # let's just make the tuple
    tlist = []
    # (`restaurant_id`,`location`,`address`,`city`,`latitude`,`longitude`,`inspected`,`critical`,`noncritical`,`updated`,`active`,`closed`,`closed_date`)
    for (id, resto) in enumerate(restos):
        restaurant_id = id
        location = resto[0]
        address = resto[1]
        city = resto[2]
        latitude, longitude = geocodes.get(resto[4], (None, None))
        inspected = updated = sqlDate(resto[3])
        critical = 0
        noncritical = 1 #FIXME
        active = 1
        if 'proposed' in location.lower(): active = 0
        closed = 0
        closed_date = 'NULL'
        tlist.append( (restaurant_id, location, address, city, latitude, longitude, inspected, critical, noncritical, updated, active, closed, closed_date) )

    sqldump(tlist)

if __name__ == '__main__':
    main()

