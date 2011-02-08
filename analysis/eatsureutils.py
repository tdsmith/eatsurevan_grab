#!/usr/bin/python

import time, datetime

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
#               'findings': [finding0, finding1, ..., findingN]}
#
# finding = ('heading', 'description', numNew, numResolved)


def sqlDate(vchdate):
    try:
        t = time.strptime(vchdate, '%d-%b-%Y')
        return time.strftime('%Y-%m-%d %H:%M:%S', t)
    except:
        return '1970-01-01 00:00:00'

def vch2datetime(vchdate):
    try:
        return datetime.datetime.strptime(vchdate, '%d-%b-%Y')
    except:
        return datetime.datetime(1970,1,1)

def is_naughty(repo, rguid):
    for inspection in repo[rguid]['inspections']:
        if (datetime.datetime.now() - vch2datetime(inspection['date'])).days > 365:
            # inspection report is >1 year old, skip it
            continue
        for finding in inspection['findings']:
            if finding[0] in [
                'TF: Trans Fat documentation is kept on site and provided to the EHO on request',
                'TF: All other foods meet the restriction of 5% trans fat or less of total fat',
                'TF: All soft spreadable margarine & oils meet  <2% trans fat content requiremen',
                'In Compliance - Food']:
                continue
            # check if there are new findings
            if finding[2] == 0: continue
            return True
    return False

