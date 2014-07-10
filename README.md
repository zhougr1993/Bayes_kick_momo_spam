Bayes_kick_momo_spam
====================

A system to determine whether user reported by others is a spammer

Content:
Script to gather the msg of spammer and the msg of users who were reported but not spammer by day from hdfs.

Using these msg as referance,train a NaiveBayes_classifier.

Some scripts to estimat the precision and recall of the classifier

A script to start web sevice,receiving an user's msg and return the probablity of this user to be a spamer.

