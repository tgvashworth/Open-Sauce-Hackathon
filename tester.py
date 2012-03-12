import re
import string
import time
import pickle
import random

start = time.time()

markov = pickle.load(open('markov.txt', 'rb'))

text = []

popular = ""
# max = 0
# for word in markov:
#   sum = 0
#   for secword in markov[word]:
#     sum += markov[word][secword]
#   if sum > max:
#     max = sum
#     popular = word

# text.append(popular)


popular = random.choice(markov)
text.append(popular)

print text

lastword = popular
for i in range(0, 10):
  nextword = ""
  max = 0
  for word in markov[lastword]:
    if markov[lastword][word] > max:
      max = markov[lastword][word]
      nextword = word

  text.append(nextword)
  lastword = nextword


print ' '.join(text)

print "Took: ", time.time() - start