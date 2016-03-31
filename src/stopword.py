from init import *
proc = proc2
stopWords = ' '.join(open('../data/stopwords.txt').read().split())
lemmas = open('../data/StopLemmas.txt','w')
for x in set(proc2.parse_doc(stopWords)['sentences'][0]['lemmas']):
	lemmas.write(x+'\n')
lemmas.close()