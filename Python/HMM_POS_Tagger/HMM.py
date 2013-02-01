#Author: Stephen Pryor
#Date: May 15, 2012
"""
A Bigram HMM POS Tagger
"""
from urn import *
import math
import sys

class HMM:
  def __init__(self, tagLexicon):
    self.tags = ["<s>", "</s>"]+tagLexicon
    self.b = {}
    for tag in self.tags:
      self.b[tag] = urn()
    self.tagEncoding = {}
    self.transitionNormTerm = {} #normalization terms
    i = 0
    for tag in self.tags:
      self.tagEncoding[tag] = i
      i = i + 1
    self.initializeTransitionMatrix()
    self.lambda1 = 0
    self.lambda2 = 0
  
  #fill the transition matrix
  def initializeTransitionMatrix(self):
    numTags = len(self.tags)
    self.transitionMatrix = []
    for i in range(numTags):
      self.transitionMatrix.append([0]*numTags)
  
  #perform deleted interpolation between the bigram and unigram model
  def deletedInterpolation(self):
    self.lambda1 = 0
    self.lambda2 = 0
    for s in self.tags:
      unigramProb = self.tagCounts[s]/self.totalTags
      for s_prev in self.tags:
        numerator = self.transitionMatrix[self.tagEncoding[s_prev]][self.tagEncoding[s]]
        if numerator > 0:
          bigramProb = 0.0
          try:
            bigramProb = float(numerator - 1.0)/(self.transitionNormTerm[s_prev] - 1.0)
          except:
            pass
          if bigramProb > unigramProb:
            self.lambda2 = self.lambda2 + numerator
          else:
            self.lambda1 = self.lambda1 + numerator
    normalizationTerm = float(self.lambda1 + self.lambda2)
    self.lambda1 = float(self.lambda1)/normalizationTerm
    self.lambda2 = float(self.lambda2)/normalizationTerm
          
  #train the model by collectin the needed counts  
  def train(self, D):
    for sentence in D:
      sentence = [("<s>", "<s>")]+sentence+[("</s>", "</s>")]
      for i in range(len(sentence)-1):
        word_current, tag_current = sentence[i]
        word_next, tag_next = sentence[i+1]
        self.b[tag_current].insertWord(word_current)
        self.transitionMatrix[self.tagEncoding[tag_current]][self.tagEncoding[tag_next]] = self.transitionMatrix[self.tagEncoding[tag_current]][self.tagEncoding[tag_next]] + 1
    #calculate the normalization terms
    self.tagCounts = {}
    for tag in self.tags:
      self.tagCounts[tag] = float(sum(self.transitionMatrix[self.tagEncoding[tag]]))
      self.transitionNormTerm[tag] = float(sum(self.transitionMatrix[self.tagEncoding[tag]]))
    self.totalTags = sum([sum(row) for row in self.transitionMatrix])
    self.deletedInterpolation()
  
  #get the transition probability P(s|s_prev)
  def transitionProb(self, s_prev, s):
    try:
      return math.log(self.lambda2*(float(self.transitionMatrix[self.tagEncoding[s_prev]][self.tagEncoding[s]])/self.transitionNormTerm[s_prev])+self.lambda1*(self.tagCounts[s_prev]/self.totalTags), 2)
    except:
      return -float("inf")
  
  #use the viterbi algorithm to produce a tag sequence for an untagged sequence of words
  def viterbiDecoder(self, sequence):
    T = len(sequence)
    N = len(self.tags)
    viterbi = []
    backpointers = {}
    for i in range(T):
      viterbi.append([0]*N)
    
    #initialization
    for t in self.tags:
      viterbi[0][self.tagEncoding[t]] = self.transitionProb("<s>", t)+self.b[t].probOfWord(sequence[0])
      backpointers[(0, t)] = 0
      
    #recursion step
    for i in range(1, T):
      for t in self.tags:
        prevLattice = {}
        for prevTag in self.tags:
          prevLattice[(i-1, prevTag)] = viterbi[i-1][self.tagEncoding[prevTag]]+self.transitionProb(prevTag, t)
        viterbi[i][self.tagEncoding[t]] = max(prevLattice.values())+self.b[t].probOfWord(sequence[i])
        backpointers[(i, t)] = max(prevLattice, key=prevLattice.get)

    #termination step
    prevLattice = {}
    for prevTag in self.tags:
      prevLattice[(T-1, prevTag)] = viterbi[T-1][self.tagEncoding[prevTag]]+self.transitionProb(prevTag, "</s>")
    finalScore = max(prevLattice.values())
    backpointers[(T, "</s>")] = max(prevLattice, key=prevLattice.get)
    
    tagSequence = []
    pointer = backpointers[(T, "</s>")]
    while pointer != 0:
      tagSequence.append(pointer[1])
      pointer = backpointers[pointer]
    tagSequence.reverse()
    return [(sequence[i], tagSequence[i]) for i in range(len(sequence))]
  
  #given a sentece of word/tag pairs, return just the sequence of words  
  def stripTags(self, taggedSentence):
    return [word for word, tag in taggedSentence]
  
  #given a test set, calculate the accuracy of the model  
  def evaluate(self, D):
    numTotal = 0
    numCorrect = 0
    numSentences = 1
    totalSentences = float(len(D))
    sys.stdout.write("  ")
    outputSize = 2
    for sentence in D:
      output = "{0:.2f}%".format((float(numSentences)/totalSentences)*100.0)
      backspaces = ""
      for j in range(outputSize):
        backspaces = backspaces + "\b"
      outputSize = len(output)
      sys.stdout.write(backspaces + output)
      numSentences = numSentences + 1
      tmpS = self.viterbiDecoder(self.stripTags(sentence))
      for i in range(len(sentence)):
        numTotal = numTotal + 1
        if sentence[i][1] == tmpS[i][1]:
          numCorrect = numCorrect + 1
    backspaces = ""
    for j in range(outputSize):
      backspaces = backspaces + "\b"
    sys.stdout.write(backspaces)
    return float(numCorrect)/float(numTotal)
