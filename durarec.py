# Copyright (c) 2016 Allison Sliter
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

def closeenough(x,y):
    xpre = x - 1
    xpost = x + 1
    return y >= xpre and y <= xpost

with open("wavs.txt", 'r') as w:
    wavs = w.read().split()
with open("textgrid.txt", 'r') as t:
    lines = t.readlines()


junk = [l.split() for l in lines]
txts = {j[0][:7] : j[2] for j in junk}

wavdict = dict()
good_dict = dict()

for x in range(0, len(wavs)-1, 2):
    name = wavs[x][:7]
    if name in wavdict.keys():
        wavdict[name].append(wavs[x+1])
    else:
        wavdict[name] = [wavs[x+1]]

    
for k in wavdict.keys():
    if k in txts.keys():
        good_dict[k] = wavdict[k]


bad = list()

for k in good_dict.keys():
    tlength = float(txts[k])
    unfound = True
    for v in good_dict[k]:
        if closeenough(tlength, float(v)):
            unfound = False
    if unfound:
        bad.append(k)

#for b in sorted(bad):
#    print b, "wavs:", good_dict[b], "texts",  txts[b]


badset = set(bad)
totalset = set(good_dict.keys())
goodset = totalset - badset

goodlist = sorted(list(goodset))

for g in goodlist:
    print g, "wavs:", good_dict[g], "texts:", txts[g]

    
