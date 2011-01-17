#!/usr/bin/python

import time

def sqlDate(vchdate):
    try:
        t = time.strptime(vchdate, '%d-%b-%Y')
        return time.strftime('%Y-%m-%d %H:%M:%S', t)
    except:
        return '1970-01-01 00:00:00'

