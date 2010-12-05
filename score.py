#!/usr/bin/python

import cPickle

f = open('inspections.repr', 'r')
buf = f.read()
f.close()

restos = eval(buf)

scores = {}

# restos = [ restos[0] ]

for resto in restos:
    guid = resto[0]
    inspections = resto[1]
    score = 0
    for inspection in inspections:
        if inspection[2] == u'Re-inspection':
            score += 1
    scores[guid] = score

f = open('scores.pickle', 'w')
cPickle.dump(scores, f, -1)
f.close()

