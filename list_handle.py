#!/usr/bin/env python
import sys
for line in sys.stdin:
    try:
        item_list = eval(line)
    except:
        print line
        continue
    for (f,l) in item_list:
        print l
        msg = ''
        for word in f.keys():
            msg += ','+ word
        print msg
