from init import *
proc = proc2
stopWords = ' '.join(open('../data/shortStops.txt').read().split())
lemmas = open('../data/sortStopLemmas.txt','w')
for x in set(proc2.parse_doc(stopWords)['sentences'][0]['lemmas']):
	lemmas.write(x+'\n')
lemmas.close()