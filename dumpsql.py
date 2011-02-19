#!/usr/bin/python
# dumpsql.py
# dumps an EatSureMySQL database from repo.repr

from eatsureutils import sqlDate, juris2city, is_naughty
import time

inspection_preamble = """
DROP TABLE IF EXISTS `inspection`;
CREATE TABLE `inspection` (
  `inspection_id` int(10) unsigned NOT NULL,
  `restaurant_id` int(10) unsigned NOT NULL,
  `severity` varchar(80) default '0',
  `inspection_type` varchar(255) NOT NULL,
  `category` varchar(255) default NULL,
  `description` varchar(255) NOT NULL,
  `inspected` datetime default NULL,
  `active` int(10) unsigned NOT NULL default '1',
  PRIMARY KEY  (`inspection_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40000 ALTER TABLE `inspection` DISABLE KEYS */;
INSERT INTO `inspection` (`inspection_id`,`restaurant_id`,`severity`,`inspection_type`,`category`,`description`,`inspected`,`active`) VALUES
"""

inspection_postscript = '/*!40000 ALTER TABLE `inspection` ENABLE KEYS */;'

restaurant_preamble = """
DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE `restaurant` (
  `restaurant_id` int(10) unsigned NOT NULL,
  `location` varchar(120) NOT NULL,
  `address` varchar(120) NOT NULL,
  `city` varchar(80) NOT NULL,
  `latitude` decimal(10,6) default NULL,
  `longitude` decimal(10,6) default NULL,
  `inspected` date default NULL,
  `critical` int(10) unsigned default NULL,
  `noncritical` int(10) unsigned default NULL,
  `updated` datetime default NULL,
  `active` tinyint(1) default '1',
  `closed` int(11) NOT NULL default '0',
  `closed_date` datetime default NULL,
  PRIMARY KEY  (`restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` (`restaurant_id`,`location`,`address`,`city`,`latitude`,`longitude`,`inspected`,`critical`,`noncritical`,`updated`,`active`,`closed`,`closed_date`) VALUES
"""
restaurant_postscript = '/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;'

update_definition = """
DROP TABLE IF EXISTS `updated`;
CREATE TABLE `updated` (
  `update_id` int(10) unsigned NOT NULL,
  `update` datetime NOT NULL,
  PRIMARY KEY  (`update_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `updated` (`update_id`,`update`) VALUES
(0,'%s');
""" % time.strftime('%Y-%m-%d %H:%M:%S')

def main():
    f = open('repo.repr', 'r')
    repo = eval(f.read())
    f.close()

    # create a normalized 'city' field from the jurisdiction data
    for guid in repo: repo[guid]['city'] = juris2city(repo[guid]['jurisdiction'])

    # assign each restaurant an integer row number
    sqlid_from_rguid = dict([(i[1], i[0]) for i in enumerate(repo.keys())])

    resto_rows = []
    for (guid, resto) in repo.items():
        d = {}
        d['restaurant_id'] = sqlid_from_rguid[guid]
        d['location'] = resto['name']
        d['address'] = resto['street']
        d['city'] = resto['city'] #note that we created this above
        d['latitude'], d['longitude'] = resto['lat'], resto['long']
        d['inspected'] = d['updated'] = sqlDate(resto['update'])
        d['critical'] = 0
        d['noncritical'] = int(is_naughty(repo, guid))
        d['active'] = 1
        d['closed'] = 0
        d['closed_date'] = 'NULL'
        
        row = '(%s)' % ','.join([repr(d[col]) for col in ['restaurant_id', 'location', 'address', 'city', 'latitude', 'longitude', 'inspected', 'critical', 'noncritical', 'updated', 'active', 'closed', 'closed_date']])
        resto_rows.append(row)

    # that was fun; let's do inspection data now
    inspection_rows = []
    inspSeq = 0
    for (rguid, resto) in repo.items():
        for insp in resto['inspections']:
            for finding in insp['findings']:
                d = {}
                d['inspection_id'] = inspSeq
                inspSeq += 1
                d['restaurant_id'] = sqlid_from_rguid[rguid]
                d['severity'] = 'Non-Critical'
                d['inspection_type'] = insp['reason']
                d['category'] = finding[0]
                d['description'] = finding[1][:254].replace('\0','').replace('\r','')
                d['inspected'] = sqlDate(insp['date'])
                d['active'] = 1
                row = '(%s)' % ','.join([repr(d[col]) for col in ['inspection_id', 'restaurant_id', 'severity', 'inspection_type', 'category', 'description', 'inspected', 'active']])
                inspection_rows.append(row)

    print restaurant_preamble
    print ',\n'.join(resto_rows), ';'
    print restaurant_postscript

    print inspection_preamble
    # pretend you don't see this please
    print (',\n'.join(inspection_rows)).replace("(u'", "('").replace('(u"', '("').replace(',u"',',"').replace(",u'",",'"), ';'
    print inspection_postscript

    print update_definition

if __name__ == '__main__':
    main()

