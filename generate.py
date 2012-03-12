import re
import string
import time
import pickle
import random

def pickword(words):
  total = 0
  for word in words:
    total += words[word]
  target = random.uniform(0, total)
  sum = 0
  for word in words:
    sum += words[word]
    if target < sum:
      return word

start = time.time()

markov = pickle.load(open('markov.txt', 'rb'))

text = []

# max = 0
# for word in markov:
#   sum = 0
#   for secword in markov[word]:
#     sum += markov[word][secword]
#   if sum > max:
#     max = sum
#     popular = word

# text.append(popular)

# print markov

nextword = random.choice(markov.keys())
text.append(nextword)

for i in range(0, 100):
  word = pickword(markov[nextword])
  text.append(word)
  nextword = word


print ' '.join(text)

print "Took: ", time.time() - start