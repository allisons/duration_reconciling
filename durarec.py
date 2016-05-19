# Copyright (c) 2016 Allison Sliter
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from sys import argv
from os import walk, path
import re
import subprocess

def close_enough(x,y):
    xpre = x - 1
    xpost = x + 1
    return y >= xpre and y <= xpost

tg_walk = walk(argv[1])
audio_files = walk(argv[2])

tg_dict = {}
root, dirs, files = tg_walk.next()
for name in files:
    with open(path.join(root, name)) as f:
        ogid = re.compile(r'OGI.{4}', re.I).findall(name)[0]
        duration = f.readlines()[1].split()[1]
        tg_dict[ogid.upper()] = float(duration)
audio_dict = {}
root, dirs, files = audio_files.next()
for name in files:
    try:
        ogid = re.compile(r'OGI.{4}', re.I).findall(name)[0]
    except:
        print "ID extraction didn't work with", name
        continue
    command = ['soxi', '-D', path.join(root,name)]
    try:
        duration = float(subprocess.check_output(command))
    except:
        print "Duration measure didn't work with this guy", name
        continue
    # print ogid, duration
    audio_dict[ogid.upper()] = duration

matched_duration = []
non_matched_duration = {}
missing_audio = []
for key in tg_dict.keys():
    if key in audio_dict:
        if close_enough(audio_dict[key], tg_dict[key]):
            matched_duration.append(key)
        else:
            non_matched_duration[key] = (tg_dict[key], audio_dict[key])
    else:
        missing_audio.append(key)

missing_textgrid = list(set(audio_dict.keys()) - set(tg_dict.keys()))
print "Mismatched duration"
print "ID \t TextGrid Duration \t Audio Duration"
if len(non_matched_duration) == 0:
    print "No mismatched textgrids/audio"
else:
    for k, v in non_matched_duration.items():
        print k +'\t'+str(v[0])+'\t'+str(v[1])
    
print "---------------------------"
print "Missing Audio"
if len(missing_audio) == 0:
    print "No missing audio"
else:
    for key in missing_audio:
        print key            
            
print "---------------------------"
print "Missing TextGrids"
if len(missing_textgrid) == 0:
    print "No missing TextGrids"
else:
    for key in missing_textgrid:
        print key            
    
