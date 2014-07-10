#!/usr/bin/env python
import datetime
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
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import socket

from tornado.options import define, options
define("port", default=9527, help="run on the given port", type=int)

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
    if classifier.prob_classify(feats).prob(lable) > Threshold:
        return True
    else:
        return False

def form_json(momoid,spam_probablity,normal_probablity):
#insert the judged info to a json
    info = {}
    info['momoid'] = momoid
    info['spam_probablity'] = spam_probablity
    info['normal_probablity'] = normal_probablity
    result = json.dumps(info)
    return result

class ProbHandler(tornado.web.RequestHandler):
    def get(self):
        momoid = self.get_argument('momoid')
        words = self.get_argument('words')
        words = words.encode('utf-8')
        momoid = momoid.encode('utf-8')
        seg = seg_words(words)
        dt = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
        try:
            feats = word_feats(seg)
            spam_p = classifier.prob_classify(feats).prob('spam')
            normal_p = classifier.prob_classify(feats).prob('normal')
            self.write(form_json(momoid,spam_p,normal_p))
            print(form_json(momoid,spam_p,normal_p))
            f = open('handle_log_'+dt,'a')
            f.write(momoid+'\t'+str(seg)+'\t'+form_json(momoid,spam_p,normal_p)+'\n')
            f.close()
        except:
            f = open('handle_log_'+dt,'a')
            f.write(momoid+'\t'+str(seg)+'\t'+'Error caculate probablity'+'\n')
            f.close()
            print "Error caculate probablity."
            self.write("Error caculate probablity.")
    def post(self):
        momoid = self.get_argument('momoid')
        words = self.get_argument('words')
        words = words.encode('utf-8')
        momoid = momoid.encode('utf-8')
        seg = seg_words(words)
        dt = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
        try:
            feats = word_feats(seg)
	    spam_p = classifier.prob_classify(feats).prob('spam')
            normal_p = classifier.prob_classify(feats).prob('normal')
            self.write(form_json(momoid,spam_p,normal_p))
            print(form_json(momoid,spam_p,normal_p))
            f = open('handle_log_'+dt,'a')
            f.write(momoid+'\t'+str(seg)+'\t'+form_json(momoid,spam_p,normal_p)+'\n')
            f.close()
        except:
            print "Error caculate probablity."
            f = open('handle_log_'+dt,'a')
            f.write(momoid+'\t'+str(seg)+'\t'+'Error caculate probablity'+'\n')
            f.close()
            self.write("Error caculate probablity.") 
if __name__ == '__main__':
    try:
        classifier = load_classifier('Spam_classifier')
    except:
        print 'Loading classifier fails'
    #Start tornado service.
    app = tornado.web.Application(handlers=[(r"/prob", ProbHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port,family=socket.AF_INET)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()
