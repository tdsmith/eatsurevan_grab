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

# print CSV
f = open('output.csv', 'w')
print >> f, 'Name,Address,Restaurant GUID,Score'
for line in buf:
    f.write(line[0] + ',')
    f.write('"' + line[1] + ', ' + line[2] + ' BC",')
    f.write(line[4] + ',')
    f.write(str(line[5]) + '\n')

