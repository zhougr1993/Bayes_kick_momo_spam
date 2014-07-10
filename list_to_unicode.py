#!/usr/bin/env python
import sys
for line in sys.stdin:
    try:
        momoid,msg = line.strip().split('\t')
        item_list = eval(msg)
    except:
        print line
        continue
    msg = ''
    for word in item_list:
        msg += ','+ word
    print momoid+'\t'+msg
