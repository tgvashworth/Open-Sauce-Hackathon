import re
import string
import time
import pickle
import os, os.path
import json
from StringIO import StringIO

def build(dic, tokens, n, i, freq):
  if n == i - 1:
    dic[tokens[n]] = freq
  else:
    if tokens[n] not in dic:
      dic[tokens[n]] = {}
    return build(dic[tokens[n]], tokens, n+1, i, freq)


def dumpchain(directory, filename):
  markov = {}
  f = open(directory + "/" + filename)
  for line in f:
    tokens = line.rstrip().split('\t')
    if len(tokens) == 0:
      continue
    freq = int(tokens.pop(0))
    build(markov, tokens, 0, len(tokens), freq)
  dump = open('chains/'+filename, 'wb')
  pickle.dump(markov, dump, pickle.HIGHEST_PROTOCOL)

start = time.time()

files = ["w1.txt", "w2.txt", "w3.txt", "w4.txt", "w5.txt"]

for f in files:
  dumpchain("data", f)

print "Took: ", time.time() - start