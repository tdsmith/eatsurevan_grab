#!/usr/bin/python

import codecs
from eatsureutils import vch2datetime, is_naughty

header = """<?xml version="1.0" encoding="UTF-8"?>
<layer>
<pois>"""

footer = """</pois>
</layer>"""

poi_template = """<poi>
    <id>%(rguid)s</id>
    <action>
        <uri>http://www.foodinspectionweb.vcha.ca/Facility/Show/%(rguid)s</uri>
        <label>See inspection report</label>
    </action>
    <lat>%(lat)s</lat>
    <lon>%(long)s</lon>
    <title>%(name)s</title>
    <line2>%(street)s</line2>
    <type>%(iconset)d</type>
</poi>"""


def main():
    f = open('repo.repr', 'r')
    repo = eval(f.read())
    f.close()

    outbuf = []
    for rguid in repo:
        repo[rguid]['rguid'] = rguid
        if is_naughty(repo, rguid):
            repo[rguid]['iconset'] = 2
        else:
            repo[rguid]['iconset'] = 1
        outbuf.append( poi_template % repo[rguid] )

    f = open('layar.xml', 'w')
    print >> f, header
    print >> f, ('\n'.join(outbuf)).replace('&', '&amp;').replace('\0','').encode('ascii', 'xmlcharrefreplace')
    print >> f, footer
    f.close()

if __name__ == '__main__':
    main()

