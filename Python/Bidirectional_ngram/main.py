#Author: Stephen Pryor
#Date: 5/15/12

import sys
from ngram import *
from bidirectional_ngram import *
from ngram_util import * 

#-----------------------------------------------------------------------START - Load the training set
sys.stdout.write("Loading training set...")
trainingSentences = getWSJDirectories(14, "c:/wsj/")
print "complete!"
#-----------------------------------------------------------------------END - Load the training set

#-----------------------------------------------------------------------START - Load the testing set
sys.stdout.write("Loading testing set...")
testingSentences = getWSJDirectories(15, "c:/wsj/", 1)
print "complete!"
#-----------------------------------------------------------------------END - Load the testing set

ngrams = [1, 2, 3, 4]

#-----------------------------------------------------------------------START - Evaluate the gram models
print "\n------------------------N-grams:\n"
for n in ngrams:
  model = ngram(n, 0.0001)
  sys.stdout.write("Training "+`n`+"-gram language model...")
  model.train(trainingSentences)
  print("complete!")
  sys.stdout.write("Evaluating model on training set...")
  print "Perplexity: "+`model.evaluate(trainingSentences)`
  sys.stdout.write("Evaluating model on testing set...")
  print "Perplexity: "+`model.evaluate(testingSentences)`
  print 
#-----------------------------------------------------------------------END - Evaluate the gram models

#-----------------------------------------------------------------------START - Evaluate the bidirectional models
print "\n------------------------Bidirectional N-grams:\n"
for n in ngrams:
  model = bidirectional_ngram(n, 0.0001)
  sys.stdout.write("Training "+`n`+"-gram language model...")
  model.train(trainingSentences)
  print("complete!")
  sys.stdout.write("Evaluating model on training set...")
  print "Perplexity: "+`model.evaluate(trainingSentences)`
  sys.stdout.write("Evaluating model on testing set...")
  print "Perplexity: "+`model.evaluate(testingSentences)`
  print
#-----------------------------------------------------------------------END - Evaluate the bidirectional models