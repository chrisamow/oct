#!/usr/bin/env python
"""
can standalone run for testing
pass textfilename as argument
"""

import sys
import stopwords
import collections
import re
from itertools import islice



def words(text):
    """return all alphanumeric words lowercased, does not filter for duplicates"""
    w = text.lower()
    w = re.findall(r"[\w]+", w) #doesnt handle single quote well

    return w

def rmstopwords(words):
    w = [x for x in words if x not in stopwords.STOPWORDS]
    w = [x for x in w if len(x)>1 ] #removing single letter words
    return w

def wordcount(words):
    cnt = collections.Counter()
    for w in words:
        cnt[w] += 1
    d = collections.OrderedDict(cnt)
    o = collections.OrderedDict(sorted(d.iteritems(), key=lambda x: x[1], reverse=True))
    return o

def max100(ordered):
    if(len(ordered)>100):
        sliced = islice(ordered.iteritems(), 100)  # o.iteritems() is o.items() in Python 3
        ordered = collections.OrderedDict(sliced)
    return ordered

def processtext(text):
    return max100(wordcount(rmstopwords(words(text))))

def jsify(counts):
    """
    javascript will need the data like this:
    list = [['foo', 12], ['bar', 6]]
    """
    pairs = ( "['{}',{}]".format(w,c)  for w,c in counts.iteritems() )
    js = '[ ' + ', '.join(pairs) + ' ]'
    return js


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as myfile:
        data = myfile.read()
        w = words(data)
        print (w)
        print ('total words: {}'.format(len(w)))
        x = rmstopwords(w)
        print (x)
        print ('without stopwords: {}'.format(len(x)))
        counts = wordcount(x)
        print ('counts: {}'.format(counts))

        z = jsify(counts)
        print ('js format: {}'.format(z))

