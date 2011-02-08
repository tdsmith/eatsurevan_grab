#!/usr/bin/python
# simplify inspection report formatting for layar's poor little browser

import codecs
from eatsureutils import vch2datetime

def main():
    f = open('repo.repr', 'r')
    repo = eval(f.read())
    f.close()
    
    for rguid, resto in repo.items():
        f = open('layar_content/%s.html' % rguid, 'w')
        print >> f, '<h1>%(name)s</h1><p>%(street)s, %(jurisdiction)s</p>' % resto
        for i in reversed([j[1] for j in sorted([ (vch2datetime(resto['inspections'][k]['date']), k) for k in xrange(len(resto['inspections'])) ])]):
                print >> f, '<h2>%s</h2>' % resto['inspections'][i]['date']
                for finding in resto['inspections'][i]['findings']:
                    print >> f, ('<h4>%s</h4><p>%s</p>' % (finding[0], finding[1])).replace('\n', '<br />').encode('ascii', 'xmlcharrefreplace')
        f.close()

if __name__ == '__main__':
    main()

