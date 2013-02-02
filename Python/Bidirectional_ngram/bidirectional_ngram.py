#Author: Stephen Pryor
#Date: 5/15/12
"""
A bidirectional n-gram language model:
"""

from ngram import * 
import math
import copy

#uses laplace (add-alpha) smoothing
class bidirectional_ngram:
  def __init__(self, n, alpha):
    self.n = int(n)
    if self.n < 1:
      print "Error in ngram constructor: n must be an integer greater than 0"
      quit(1)
    self.models = {"lr": ngram(n, alpha), "rl": ngram(n, alpha, True)}
    self.filler = ["<s>" for i in range(self.n-1)]
    self.lambda1 = .5
    self.lambda2 = .5
  
  #given a list of sentences (a list of lists)
  #train the n-gram using the sentences
  def train(self, D):
    T = copy.deepcopy(D)
    self.models["lr"].train(T)
    self.models["rl"].train(T)
    
  #get the probability of a sentence
  def prob(self, sentence):
    P = 0.0
    #get left-right grams
    LRgrams = []
    tmpSentence = self.filler+sentence
    for i in range(len(tmpSentence)-self.n+1):
      prevGram = [tmpSentence[i+j] for j in range(self.n-1)]
      gram = tuple(prevGram+[tmpSentence[i+self.n-1]])
      prevGram = tuple(prevGram)
      LRgrams.append((prevGram, gram))
    #get right-left grams
    RLgrams = []
    sentence.reverse()
    tmpSentence = self.filler+sentence
    for i in range(len(tmpSentence)-self.n+1):
      prevGram = [tmpSentence[i+j] for j in range(self.n-1)]
      gram = tuple(prevGram+[tmpSentence[i+self.n-1]])
      prevGram = tuple(prevGram)
      RLgrams.append((prevGram, gram))
    RLgrams.reverse()
    for i in range(len(LRgrams)):
      P = P + math.log(self.lambda1*math.pow(2, self.models["lr"].probGram(LRgrams[i][1], LRgrams[i][0]))+self.lambda2*math.pow(2, self.models["rl"].probGram(RLgrams[i][1], RLgrams[i][0])), 2)
    return P
    
  #get the perplexity score of the model on some data
  def evaluate(self, T):
    D = copy.deepcopy(T)
    numtokens = 0
    totalProb = 0.0
    for sentence in D:
      numtokens = numtokens + len(sentence)
      totalProb = totalProb + self.prob(sentence)
    return math.pow(2, -totalProb/numtokens)
  