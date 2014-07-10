#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import jieba
import string
import jieba.posseg as pseg
import time
def filter_str(instr):
# filter some Symbol
    deEstr = string.punctuation + ' ' + string.digits + string.letters
    deCstr = '，。《》【】（）！？★”“、：…'
    destr = deEstr + deCstr
    outstr = ''
    for char in instr.decode('utf-8'):
        if char not in destr.decode('utf-8'):
            outstr += char
    return outstr
def get_words_rate(instr):
#Segment words in Chinese and filter out stop words then get the words' rate
    b = filter_str(instr)
    words=pseg.cut(b)
    wordtable={}
    f = open('./Swords.txt','r')
    filelines = f.readlines()
    SWstr = ''
    for x in filelines:
        if x[-1] == '\n':
            x = x[0:-1]
            SWstr = SWstr + x
    f.close()
    for w in words:
        if w.word not in SWstr.decode('utf-8'):
            wordtable[w.word] = wordtable.get(w.word,0) + 1
        else:
            pass
    return wordtable
def seg_words(instr):
#Segment words in Chinese and filter out stop words.
    b = filter_str(instr)
    words=pseg.cut(b)
    seg_list = []
    f = open('./Swords.txt','r')
    filelines = f.readlines()
    SWstr = ''
    for x in filelines:
        if x[-1] == '\n':
            x = x[0:-1]
            SWstr = SWstr + x
    f.close()
    for w in words:
        if w.word not in SWstr.decode('utf-8'):
            seg_list.append(w.word)
        else:
            pass
    return seg_list
'''
s = "我一贯认为，我们必须首先从客户体验出发，继而再回头考虑技术上的可行性。不能一味钻研技术然后再考虑可以把它用到什么产品上，以及用什么办法把它卖掉。我犯过这个错误可能比在场的任何人都要多。伤痕历历在目。我一贯认为，我们必须首先从客户体验出发，继而再回头考虑技术上的可行性。不能>一味钻研技术然后再考虑可以把它用到什么产品上，以及用什么办法把它卖掉。我犯过这个错误可能比在场的任何人都要多。伤痕历历在目"
print s
s = "力口妹妹QQ 可约"
test = seg_words(s)
start_time = time.time()
test = seg_words(s)
end_time = time.time()
sys.stdout.write("%.4g seconds.\n" % (end_time - start_time))
for x in test:
    print x
print test
'''
