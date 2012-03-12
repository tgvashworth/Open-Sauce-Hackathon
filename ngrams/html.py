import re
import string
import time
import pickle
import os, os.path

def findFreq(tokens, dic, depth, maxdepth):
  if tokens[depth] in dic and depth == maxdepth:
    return dic[tokens[depth]]
  if tokens[depth] not in dic:
      return 0
  return findFreq(tokens, dic[tokens[depth]], depth+1, maxdepth)

def restorechain(directory, filename):
  return pickle.load(open(directory + "/" + filename, 'rb'))

starttime = time.time()

files = ["w1.txt", "w2.txt", "w3.txt"]

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

# words = words[0:20]
# print words

freq = []
for x in range(0, len(files)):
  freq.append([])
  for y in range(0, len(words)):
    freq[x].append(0.0)

weights = [1, 100, 1000, 10000, 100000]
start = 0

for n in range(start, len(files)):
  order = n + 1
  for k,w in enumerate(words[:len(words)-n]):
    tokens = words[k:k+order]
    f = findFreq(tokens, markov[n], 0, n) * weights[n]
    for q in range(0, order):
      freq[n][k+q] += f

print markov[1]['of']['the']
print findFreq(['of','the'], markov[1], 0, 1)

mi = []
ma = []
for i in range(start, len(files)):
  mi.append(min(freq[i]))
  ma.append(max(freq[i]))

print mi
print ma

html = []

for k, word in enumerate(words):
  colors = []
  for i in range(start, len(files)):
    colors.append((freq[i][k] - mi[i]) / (ma[i] - mi[i]))
    # colors.append(freq[i][k])
  html.append('<span style="color:rgba('+str(int(255 * colors[0]))+','+str(int(255 * colors[1]))+','+str(int(255 * colors[2]))+',1)">' + word + '</span>')

output = open('htmloutput.html', 'w')
output.write("<!doctype html>")
output.write(' '.join(html))

print "Took: ", time.time() - starttime