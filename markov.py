import re
import string
import time
import pickle
import os, os.path

start = time.time()

corpus = open('corpus.txt', 'r').read()

words = corpus.split(' ')

markov = {}

for word in words:
  if word not in markov:
    markov[word] = {}

sum = 0.0
count = 1
for word in words[1:]:
  w = words[count-1]
  if word not in markov[w]:
    markov[w][word] = 1
  else:
    markov[w][word] += 1
  sum += 1
  count += 1

for a in markov:
  for b in markov[a]:
    markov[a][b] = markov[a][b]/sum

print sum

dump = open('markov.txt', 'wb')
pickle.dump(markov, dump)

print "Took: ", time.time() - start
