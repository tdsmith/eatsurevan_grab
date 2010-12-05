#!/usr/bin/python
#
# mkcsv.py
# Creates a CSV file suitable for upload to Google Fusion Tables for geocoding.
# Depends on scores.pickle and restos.tab.

import cPickle

# parse restaurants
f = open('restos.tab')
buf = f.readlines()
f.close()
buf = [line[:-1].split('\t') for line in buf]

# fields:
# 0: name
# 1: address
# 2: neighborhood
# 3: inspection date
# 4: guid

# open scores
f = open('scores.pickle', 'r')
scores = cPickle.load(f)
f.close()

# correlate
for line in buf:
    if line[4] in scores:
        line.append(scores[line[4]])
    else:
        line.append(0)

# open the jurisdiction table
f = open('jurisdictions.tab', 'r')
jurisbuf = f.readlines()
f.close()
jurisbuf = [line[:-1].split('\t') for line in jurisbuf]
juris = {}
for line in jurisbuf:
    juris[line[0]] = line[1]

# print CSV
f = open('output.csv', 'w')
print >> f, 'Name,Address,Restaurant GUID,Score,URL'
for line in buf:
    # Bellas seems to be a VCH term for regions accessible by the Chilcotin-
    # Bella Coola Highway (Route 20)? In any case, they're difficult to geocode
    # properly. There are about 50 of them in the data set.
    if line[2] == 'Bellas': continue
    
    # Also skip the Cypress Mountain Day Lodge, because I don't know where
    # to put it.
    if line[2] == 'North Shore Residential': continue

    # "Water - Misc" seems to be mostly temporary Whistler Olympic venues
    # that have since shut down, plus a single restaurant accessible by boat,
    # neither of which lend themselves to bulk geocoding by street address.
    if line[2] == 'Water - Misc': continue

    # "no address" seems to geocode to "bermuda," so:
    if not line[1]: continue # don't bother if we don't have an address

    # Ignore "proposed" eateries since they don't exist:
    if 'proposed' in line[0] or 'Proposed' in line[0]: continue

    # Still with us? Normalize the jurisdiction field.
    line[2] = juris[line[2]]

    # Include a URL in the data set so people can click into it from Fusion
    # Tables
    url = 'http://www.foodinspectionweb.vcha.ca/Facility/Show/' + line[4]

    f.write('"' + line[0] + '",')
    f.write('"' + line[1] + ', ' + line[2] + ' BC",')
    f.write(line[4] + ',')
    f.write(str(line[5]) + ',')
    f.write(url + '\n')

