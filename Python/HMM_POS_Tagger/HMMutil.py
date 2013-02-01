#Author: Stephen Pryor
#Date: May 15, 2012

import re
import os

_re_equals = re.compile("=+")
_re_brackets = re.compile("(\\[|\\])+")
_re_nonAlphaNumericCharacters = re.compile("[^A-Za-z0-9_/ ]")

#a function to read in and tokenize a WSJ format pos file
#return s a list of tokenized sentences
def tokenizeWSJPOSFile(filePath):
  openedFile = open(filePath)
  sentences = []
  sentence = []
  output = ""
  for line in openedFile:
    line = _re_equals.sub("", line)
    line = _re_brackets.sub(" ", line)
    line = _re_nonAlphaNumericCharacters.sub("", line)
    line = line.strip()
    line = line.lower()
    if line != "":
      for pair in line.split(" "):
        word = pair.split("/")
        if len(word) == 2:
          POS = word[1].strip()
          word = word[0].strip()
          if word != "":
            sentence.append((word, POS))
    else:
      if len(sentence) > 0:
        sentences.append(sentence)
        sentence = []
  if len(sentence) > 0:
    sentences.append(sentence)
  openedFile.close()
  return sentences

#reads and tokenizes every files in a directory assuming each
#is a WSJ style pos file
def getDirectoryContents(maxNumDocs, **kwargs):
  D = []
  for key in kwargs:
    numDocs = 0
    listing = os.listdir(kwargs[key])
    for filePath in listing:
      if numDocs == maxNumDocs:
        break
      D = D + tokenizeWSJPOSFile(kwargs[key]+filePath)
      numDocs = numDocs + 1
  return D

#used to point to a directory holding the WSJ pos file directories 
#(each with the .pos sentences files)
def getWSJDirectories(maxNumFiles, wsjLocation, startFile=0):
  D = []
  numDocs = 0
  listing = os.listdir(wsjLocation)
  for filePath in listing:
    if numDocs >= startFile:
      if numDocs-startFile == maxNumFiles:
        break
      if os.path.isdir(wsjLocation+filePath):
        D = D + getDirectoryContents("all", WSJ=wsjLocation+filePath+"/")
    numDocs = numDocs + 1
  return D

#extracts a lexicon of words and tags from a dataset of sentences
def extractLexicon_and_Tags(sentences):
  lexicon = {}
  tags = {}
  for sentence in sentences:
    for word, tag in sentence:
      lexicon[word] = 0
      tags[tag] = 0
  return lexicon.keys(), tags.keys()
  