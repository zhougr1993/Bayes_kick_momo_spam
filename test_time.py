#!/usr/bin/env python
import time
import collections, itertools
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from HandleSentence import seg_words
import sys
import pickle

def load_classifier(file_classify):
#Load classifier trained before from pickle.
    start_time = time.time()
    fp = open(file_classify)
    classifier = pickle.load(fp)
    fp.close()
    end_time = time.time()
    sys.stdout.write("%.4g seconds.\n" % (end_time - start_time))
    return classifier

def word_feats(words):
#generate the dict classifier can handle
        return dict([(word, True) for word in words])

def judge_user(classifier,words,Threshold,lable):
#use classifier to judge user's lable
    feats = word_feats(words)
    print classifier.prob_classify(feats).prob(lable)
    if classifier.prob_classify(feats).prob(lable) > Threshold:
        return True
    else:
        return False

if __name__ == '__main__':
    try:
        Spam_classifier = load_classifier('Spam_classifier')
    except:
        print 'Loading classifier fails'
    f = open('test_result_20140709','w')
    for line in sys.stdin:
        line = line.strip()
        momoid,msg = line.split('\t')
        msg = eval(msg)
        if judge_user(Spam_classifier,msg,0.9,'spam'):
            f.write(momoid+'\t'+str(msg)+'\n')
    f.close()
