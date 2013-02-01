#Author: Stephen Pryor
#Date: May 15, 2012

import math

#this class contains is used to calculate the state
#observation likelihoods for a given state
class urn:
  def __init__(self):
    self.urn = {}
    self.numWords = 0.0
    self.alpha = .00001 #smoothing parameter
  
  def insertWord(self, word):
    self.numWords = self.numWords + 1.0
    try:
      self.urn[word] = self.urn[word] + 1
    except:
      self.urn[word] = 1
      
  def probOfWord(self, word):
    denominator = self.numWords+self.alpha
    try:
      return math.log(float(self.urn[word])/denominator, 2)
    except:
      #smoothing for unknown words
      #if the word is unknown, return a very small probability
      #this is a bit of a variation on laplace add-alpha smoothing
      if self.numWords > 0.0:
        return math.log(self.alpha/denominator, 2)
      else:
        return -float("inf")
      