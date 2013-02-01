#Author: Stephen Pryor
#Date: May 15, 2012

from HMM import *
from HMMutil import *
import sys

wsjLocation = "c:/wsj/"
#-----------------------------------------------------------------------START - Load the training set
sys.stdout.write("Loading training set...")
trainingSentences = getWSJDirectories(5, wsjLocation)
print "complete!"
#-----------------------------------------------------------------------END - Load the training set

#-----------------------------------------------------------------------START - Load the testing set
sys.stdout.write("Loading testing set...")
testingSentences = getWSJDirectories(6, wsjLocation, 7)
print "complete!"
#-----------------------------------------------------------------------END - Load the testing set

#-----------------------------------------------------------------------START - Extract the lexicon and tags
sys.stdout.write("Extracting lexicon and tags...")
lexicon, tags = extractLexicon_and_Tags(trainingSentences)
print "complete!"
#-----------------------------------------------------------------------END - Extract the lexicon and tags

model = HMM(tags)

#-----------------------------------------------------------------------START - Train the model
sys.stdout.write("Training model...")
model.train(trainingSentences)
print "complete!"
#-----------------------------------------------------------------------END - Train the model

#-----------------------------------------------------------------------START - Evaluate the model on the training set
sys.stdout.write("Evaluating on training set...")
print "{0:.2f}% accuracy".format(model.evaluate(trainingSentences[:100])*100.0)
#-----------------------------------------------------------------------END - Evaluate the model on the training set

#-----------------------------------------------------------------------START - Evaluate the model on the testing set
sys.stdout.write("Evaluating on testing set...")
print "{0:.2f}% accuracy".format(model.evaluate(testingSentences[:100])*100.0)
#-----------------------------------------------------------------------END - Evaluate the model on the testing set
