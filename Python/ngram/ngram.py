#Author: Stephen Pryor
#Date: 5/13/12
"""
An n-gram language model:
The following code can be used to create n-gram language models 
using simple laplace add alpha smoothing. This smoothing is not very
good in practice but it works okay for a simple implementation
like this.
"""

import math

#uses laplace (add-alpha) smoothing
class ngram:
  def __init__(self, n, alpha, reverse=False):
    self.n = int(n)
    if self.n < 1:
      print "Error in ngram constructor: n must be an integer greater than 0"
      quit(1)
    self.alpha = float(alpha)
    self.reverse = reverse
    self.grams = {}
    self.prevGrams = {}
    self.unigramCounts = {}
    self.filler = ["<s>" for i in range(self.n-1)]
    self.V = 0
  
  #adds an n-gram to the count
  def addGram(self, gram):
    try:
      self.grams[gram] = self.grams[gram] + 1
    except:
      #add the case for an unknown word
      self.grams[tuple([gram[i] if i != len(gram) - 1 else "<UNK>" for i in range(len(gram))])] = 1
      self.grams[gram] = 1
  
  #adds the n-gram to the count, used in the denominator calculations of the prob
  def addPrevGram(self, prevGram):
    try:
      self.prevGrams[prevGram] = self.prevGrams[prevGram] + 1
    except:
      self.prevGrams[prevGram] = 1
  
  #adds a word to the unigram list (which also holds the vocabulary)
  def addUnigramCounts(self, gram):
    try:
      self.unigramCounts[gram] = self.unigramCounts[gram] + 1
    except:
      self.unigramCounts[gram] = 1
  
  #given a list of sentences (a list of lists)
  #train the n-gram using the sentences
  def train(self, D):
    for sentence in D:
      if self.reverse:
        sentence.reverse()
      sentence = self.filler+sentence
      for i in range(len(sentence)-self.n+1):
        prevGram = [sentence[i+j] for j in range(self.n-1)]
        gram = tuple(prevGram+[sentence[i+self.n-1]])
        #update numerator counts
        self.addGram(gram)
        #update denominator counts
        prevGram = tuple(prevGram)
        self.addPrevGram(prevGram)
        #update unigram counts
        self.addUnigramCounts(sentence[i+self.n-1])
      #get the last prevGram
      self.addPrevGram(tuple([sentence[len(sentence)-self.n+1+j] for j in range(self.n-1)]))
    self.V = float(len(self.unigramCounts.keys()))
    self.totalNumberOfWords = float(sum([self.unigramCounts[word] for word in self.unigramCounts.keys()]))
  
  #get the probability of an n-gram
  def probGram(self, gram, prevGram):
    gramCount = 0
    try:
      gramCount = self.grams[gram]
    except:
      #if the current gram is not known, try to replace the first word with the <UNK> word
      try:
        gramCount = self.grams[tuple([gram[i] if i != len(gram) - 1 else "<UNK>" for i in range(len(gram))])]
      except:
        pass
    preGramCount = 0
    try:
      preGramCount = self.prevGrams[prevGram]
    except:
      pass
    if self.n == 1:
      return math.log((float(gramCount)+self.alpha)/(self.totalNumberOfWords + self.alpha*self.V), 2)
    else:
      return math.log((float(gramCount)+self.alpha)/(float(preGramCount) + self.alpha*self.V), 2)
  
  #get the probability of a sentence
  def prob(self, sentence):
    P = 0.0
    if self.reverse:
      sentence.reverse()
    sentence = self.filler+sentence
    for i in range(len(sentence)-self.n+1):
      prevGram = [sentence[i+j] for j in range(self.n-1)]
      gram = tuple(prevGram+[sentence[i+self.n-1]])
      prevGram = tuple(prevGram)
      P = P + self.probGram(gram, prevGram)
    return P
  
  #get the perplexity score of the model on some data
  def evaluate(self, D):
    numtokens = 0
    totalProb = 0.0
    for sentence in D:
      numtokens = numtokens + len(sentence)
      totalProb = totalProb + self.prob(sentence)
    return math.pow(2, -totalProb/numtokens)
