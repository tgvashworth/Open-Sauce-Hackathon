import re
import string
import time
import pickle
import os, os.path
import math
import json

def freqToColor(colors, word):
  return '<span style="color:rgba('+str(colors[0])+','+str(colors[1])+','+str(colors[2])+',1)">' + word + '</span>\n'

def weightedAvgToAlpha(avg, word):
  return '<span style="color:rgba(0,0,0,'+str(1 - avg)+')">' + word + '</span>\n'

def scaledOutput(data, word):
  return '<span data-rf="'+json.dumps(data)+'">' + word + '</span>\n'

def findFreq(tokens, dic, depth, maxdepth):
  if tokens[depth] in dic and depth == maxdepth:
    return dic[tokens[depth]]
  if tokens[depth] not in dic:
      return 0
  return findFreq(tokens, dic[tokens[depth]], depth+1, maxdepth)

def restorechain(directory, filename):
  return pickle.load(open(directory + "/" + filename, 'rb'))

starttime = time.time()

files = ["w1.txt", "w2.txt", "w3.txt", "w4.txt", "w5.txt"]

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

weights = [1, 1, 1, 1, 1]
start = 0
usemax = True

for n in range(start, len(files)):
  order = n + 1
  for k,w in enumerate(words[:len(words)-n]):
    tokens = words[k:k+order]
    f = findFreq(tokens, markov[n], 0, n) #* weights[n]
    for q in range(0, order):
      if usemax:
        freq[n][k+q] = max([f, freq[n][k+q]])
      else:
        freq[n][k+q] += f

#print markov[1]['of']['the']
#print findFreq(['of','the'], markov[1], 0, 1)

mi = []
ma = []
for i in range(start, len(files)):
  mi.append(float(min(freq[i])))
  ma.append(float(max(freq[i])))

#print mi
#print ma

html = []
alpha = 0.05

for k, word in enumerate(words):
  data = []
  for i in range(start, len(files)):
    freq[i][k] = (freq[i][k] - mi[i]) / (ma[i] - mi[i])
    data.append(freq[i][k])
  html.append(scaledOutput(data, word))

output = open('output/htmloutput'+str(time.time())+'.html', 'w')
output.write("""<!doctype html><style>body { background:black; font-family: monospace; line-height: 1.3; }</style>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script>
  var weights = [1000,10,1,100,1000]
    , alpha = 0.1;

  $(window).load(function () {
    console.log("hello");

    reload()

    $('#alpha').val(alpha).change(function () { alpha = parseFloat($(this).val()); reload() })
    $('#w1').val(weights[0]).change(function () { weights[0] = parseFloat($(this).val()); reload() })
    $('#w2').val(weights[1]).change(function () { weights[1] = parseFloat($(this).val()); reload() })
    $('#w3').val(weights[2]).change(function () { weights[2] = parseFloat($(this).val()); reload() })
    $('#w4').val(weights[3]).change(function () { weights[3] = parseFloat($(this).val()); reload() })
    $('#w5').val(weights[4]).change(function () { weights[4] = parseFloat($(this).val()); reload() })

    function reload() {
      $('span').each(function() {
        var data = $(this).data('rf');
        var total = 0, l=data.length;
        var sum = 0;
        for(var i=0; i<l; i++) {
          sum += weights[i];
          total += data[i] * weights[i];
        }
        var avg = 0
        if(sum !== 0) {
          avg = Math.pow((total / sum), alpha);
        }
        $(this).css({color: 'rgba(0,255,0,'+(Math.max(1-avg, 0.1))+')'});
      })
    }

  })

</script>
<div>
Alpha:
<input type=text id="alpha">
</div>
<div>
W1:
<input type=text id="w1">
</div>
<div>
W2:
<input type=text id="w2">
</div>
<div>
W3:
<input type=text id="w3">
</div>
<div>
W4:
<input type=text id="w4">
</div>
<div>
W5:
<input type=text id="w5">
</div>""")
output.write(' '.join(html))

print "Took: ", time.time() - starttime