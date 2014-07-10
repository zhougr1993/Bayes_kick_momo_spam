#!/usr/bin/env python
import collections, itertools
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import pickle
import re

class sample():
#class to storage sample's lable and content
    def __init__(self, lable_x, x_table, lable_y,y_table):
        self.lable_x = lable_x
        self.lable_y = lable_y
        self.x_table = x_table
        self.y_table = y_table
    def words(self,key):
        return self.x_table.get(key,[])+self.y_table.get(key,[])
    def fileids(self,lable):
        if self.lable_x == lable:
            return self.x_table.keys()
        if self.lable_y == lable:
            return self.y_table.keys()
        return None

class generate_classifier():
#generate a classifier
    def generate(self,sample):
        lable_x = sample.lable_x
        lable_y = sample.lable_y
        x_ids = sample.fileids(lable_x)
        y_ids = sample.fileids(lable_y)
        x_feats = [(self.word_feats(sample.words(f)), lable_x) for f in x_ids]
        y_feats = [(self.word_feats(sample.words(f)), lable_y) for f in y_ids]
        x_train_num = len(x_feats)*3/4
        y_train_num = len(y_feats)*3/4
        testfeats = x_feats[x_train_num:]+y_feats[y_train_num:]
        trainfeats = x_feats[:x_train_num]+y_feats[:y_train_num]
        classifier = NaiveBayesClassifier.train(trainfeats)
        print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
        #classifier.show_most_informative_features()
        precision,error_list = self.precision(classifier,testfeats,'spam',0.999)
        recall,miss_list = self.recall(classifier,testfeats,'spam',0.999)
        print 'spam precision' + str(precision)+'-------------------'
        print error_list
        print 'spam recall' + str(recall)+'-----------------------'
        print miss_list
        return classifier
    def recall(self,classify,gold,lable,Threshold):
        result = []
        lable_list = []
        for (f,l) in gold:
            if l==lable:
                lable_list.append((f,l))
                if classify.prob_classify(f).prob(lable) >  Threshold:
                    result.append((f,l))
        return float(len(result))/len(lable_list),[x for x in lable_list if x not in result]
    def precision(self,classify,gold,lable,Threshold):
        result = []
        correct_list = []
        for (f,l) in gold:            
            if classify.prob_classify(f).prob(lable) > Threshold:
                if lable == l:
                    correct_list.append((f,l))
                result.append((f,l))
        return float(len(correct_list))/len(result),[x for x in result if x not in correct_list]
    def word_feats(self,words):
        return dict([(word, True) for word in words])

def load_classifier(file):
#Load classifier trained before from pickle.
    start_time = time.time()
    sys.stdout.write("Loading classifier in:")
    sys.stdout.flush()
    fp = open(file)
    classifier = pickle.load(fp)
    fp.close()
    end_time = time.time()
    sys.stdout.write("%.4g seconds.\n" % (end_time - start_time))
    return classifier

if __name__ == '__main__':
    f = open('spam_msg_20140707','r')
    spam_msg_sample = {}
    for line in f.readlines():
        line = line.strip()
        momoid,msg = line.split('\t')
        spam_msg_sample[momoid] = eval(msg)
    f.close()
    f = open('normal_msg_20140707','r')
    normal_msg_sample = {}
    for line in f.readlines():
        line = line.strip()
        momoid,msg = line.split('\t')
        normal_msg_sample[momoid] = eval(msg)
    f.close()
    train_sample = sample('spam',spam_msg_sample,'normal',normal_msg_sample)
    Bayes_generate = generate_classifier()
    Spam_classifier = Bayes_generate.generate(train_sample)
    #pickle.dump(Spam_classifier,open('Spam_calssifier','wb'))
