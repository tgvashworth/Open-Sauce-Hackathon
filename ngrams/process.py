import re
import string
import time
import pickle
import os, os.path

def findFreq(tokens, dic, n, i):
  if tokens[n] not in dic:
      return 0
  if n == i - 1:
      return dic[tokens[n]]
  return findFreq(tokens, dic[tokens[n]], n+1, i)

def restorechain(directory, filename):
  return pickle.load(open(directory + "/" + filename, 'rb'))

start = time.time()

files = ["w1.txt", "w2.txt", "w2.txt"]

markov = []

for f in files:
  markov.append(restorechain("chains", f))

words = []

for line in open("text/article.txt", 'r'):
  line = line.lower().rstrip()
  line = re.sub(r"(\d)", '', line)
  line = re.sub(r"(\s+)", ' ', line)
  if line == "":
    continue
  exclude = set(string.punctuation)
  buf = ""
  for ch in line:
    if ch not in exclude:
      buf += ch
    else:
      if ch not in set(['\'']):
        buf += ' '
  line = buf
  line = re.sub(r"(\s+)", ' ', line)
  lwords = line.split(' ')
  for x in range(0, lwords.count('')):
    lwords.remove('')
  words.extend(lwords)

freq = [0] * len(words)
weights = [1, 1000, 1000000, 1000000000, 1000000000]

for n in range(0, len(files)):
  order = n + 1
  for k, word in enumerate(words[n:]):
    tokens = []
    for i in range(0, order):
      tokens.append(words[k-order+1+i])
    tf = findFreq(tokens, markov[n], 0, order) * weights[n]
    for i in range(0, order):
      freq[k-order+1+i] += tf

print freq[0:10]

print "Took: ", time.time() - start