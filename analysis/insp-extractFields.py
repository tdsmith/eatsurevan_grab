#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
from eatsureutils import sqlDate
import glob, sys, os, codecs

inspfiles = glob.glob('../inspections/*html')

def parseInspections(filenames, inspection_owners, startSeq = 0):
    # d = {}
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    print """/*!40000 ALTER TABLE `inspection` DISABLE KEYS */;
INSERT INTO `inspection` (`inspection_id`,`restaurant_id`,`severity`,`inspection_type`,`category`,`description`,`inspected`,`active`) VALUES """
    outstrings = []

    for (i, filename) in enumerate(inspfiles):
        # this is an old inspection file: we don't have a record of it anymore
        # probably, we should delete it.
        if not os.path.basename(filename)[:-5] in inspection_owners: continue

        print >> sys.stderr, float(i)/len(inspfiles)
        f = open(filename, 'r')
        soup = BeautifulSoup(f.read())
        f.close()

        # inspection date
        inspDate = soup.find('th', text='Inspection Date: ').findNext('td').text
        inspReason = soup.find('th', text='Reason for Inspection: ').findNext('td').text


        # extract the violation headings
        headings = soup.findAll('h4')
        for heading in headings:
            vio = heading.text.strip()
            # d[vio] = d.setdefault(vio, 0) + 1
            vioTable = heading.parent.parent.findAll('td')
            obsNew = vioTable[1].text
            obsResolved = vioTable[2].text
            vioText = '\n'.join([i.text for i in heading.findNextSiblings('p')])
# (`inspection_id`,`restaurant_id`,`severity`,`inspection_type`,`category`,`description`,`inspected`,`active`)
            outstrings.append( '(%d,%d,"%s","%s","%s","%s","%s",1)' % (startSeq,
                    inspection_owners[os.path.basename(filename)[:-5]],
                    'Non-Critical',
                    inspReason,
                    vio,
                    vioText.replace('"', '\\"').replace('\0','').replace('\r','')[:254],
                    sqlDate(inspDate)) )
            startSeq += 1
    print ',\n'.join(outstrings), ';'
    print '/*!40000 ALTER TABLE `inspection` ENABLE KEYS */;'
        

def main(startSeq = 0, startDate='01-Jan-1990'):
    # startSeq is the starting inspection finding number
    # startDate will ignore all findings before the given date (TODO)

    # load restos.tab
    f = open('../restos.tab')
    buf = f.readlines()
    f.close()
    restos = [line[:-1].split('\t') for line in buf]

    # assign an ID to each restaurant
    restaurant_sql_ids = {}
    for (i, line) in enumerate(restos):
        restaurant_sql_ids[line[4]] = i

    # build a table to assign inspections to restaurants
    f = open('../inspections.repr')
    inspections = eval(f.read())
    f.close()
    rID_by_inspection = {}
    for resto in inspections:
        for inspection in resto[1]:
            rID_by_inspection[inspection[0]] = restaurant_sql_ids[resto[0]]

    parseInspections(inspfiles, rID_by_inspection, startSeq)

if __name__ == '__main__':
    main(*sys.argv[1:])

