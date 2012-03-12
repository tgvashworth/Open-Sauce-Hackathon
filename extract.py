import re
import string
import time
import pickle
import os, os.path

start = time.time()

dump = open('corpus.txt', 'w')

def extract(direc, filename):
  # f = open(direc + '/' + filename, 'r').read().lower()
  for line in open(direc + '/' + filename, 'r'):
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
    words = line.split(' ')
    for x in range(0, words.count('')):
      words.remove('')
    line = ' '.join(words) + ' '
    line = re.sub(r"(\s+)", ' ', line)
    dump.write(line.rstrip() + ' ')

# - - - - - - - - - - - - - - - -

direc = "training"

for name in os.listdir(direc):
  print name
  extract(direc, name)

print "Took: ", time.time() - start