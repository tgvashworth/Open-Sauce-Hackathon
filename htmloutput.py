import re
import string
import time
import pickle
import random
import math

def codelength(val):
  if val == 0:
    return 0
  return -math.log(val, 2)

start = time.time()

markov = pickle.load(open('markov.txt', 'rb'))

words = []

for line in open("essay.txt", 'r'):
  #f = ' '.join(line.split('\r\n'))
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

probs = [0]

count = 1
ma = 0.0
mi = 0.0
for word in words[1:]:
  prevword = words[count-1]
  cword = words[count]
  if prevword not in markov or cword not in markov[prevword]:
    probs.append(0)
  else:
    probs.append(markov[prevword][cword])
    if markov[prevword][cword] > ma:
      ma = markov[prevword][cword]
    if markov[prevword][cword] < mi:
      mi = markov[prevword][cword]
  count += 1

html = []
print ma, mi


for k, v in enumerate(probs[1:]):
  probs[k-1] = (probs[k-1] - mi) / (ma - mi)
  #pwordcol = (probs[k-1] - min) / (max - min)
  #probs[k-1] = (cwordcol + pwordcol) / 2
  html.append('<span style="color:rgba(0,0,0,' + str(1 - probs[k-1] ** 2) + ')">' + words[k-1] + '</span>')

output = open('htmloutput.html', 'w')
output.write("<!doctype html>")
output.write(' '.join(html))

print "Took: ", time.time() - start