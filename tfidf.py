# run using python tfidf.py
from gensim import corpora, models, similarities
from stanford_corenlp_pywrapper import CoreNLP
import sys
import pprint
pp = pprint.PrettyPrinter(indent=2)
# CoreNLP initialization
proc = CoreNLP(configfile='simple.ini', corenlp_jars=["./stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*"])
# Tokenization
tokenized = proc.parse_doc(open('wiki.txt').read())
questionList = [proc.parse_doc(q)['sentences'][0]['lemmas'] for q in open('questions.txt').read().split('\n')]

# Extracting tokenized sentences
sentenceList = [s['lemmas'] for s in tokenized['sentences']]
numSentences = len(sentenceList)

# Generating dictionary
dictionary = corpora.Dictionary(sentenceList+questionList)
# dictionary.save('/tmp/corpDict.dict')

# Converting corpus and questions to vector representation
corpusVectors = [dictionary.doc2bow(c) for c in sentenceList]
qBOW = [dictionary.doc2bow(c) for c in questionList]

# corpora.MmCorpus.serialize('/tmp/corpVect.mm', corpusVectors)
# dictionary = corpora.Dictionary.load('/tmp/corpDict.dict')
# corpus = corpora.MmCorpus('/tmp/corpVect.mm')

# Initializing TF-IDF model
tfidf = models.TfidfModel(corpusVectors)

# Extracting TF-IDF of documents
corpusTfidf = tfidf[corpusVectors]
index = similarities.SparseMatrixSimilarity(corpusTfidf,num_features=len(dictionary),num_best=2)

# index.save('/tmp/deerwester.index')
# index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
sims=[]
# Similarity computation
for q in qBOW:
	sims.append(index[tfidf[q]])
# pp.pprint(sims)
sortedAnswers=[]
for answerSentences in sims:
	answerSentences = sorted(answerSentences, key=lambda tup: tup[1], reverse=True)
	sortedAnswers.append(answerSentences)
# print(sortedAnswers)
# sortedSims.filter(lambda tup:tup[0]<numSentences)
for s in sortedAnswers:
	for x in s:
		print 'Potential sentence (score:%.2f' % (x[1],),'):',
		print ' '.join(tokenized['sentences'][x[0]]['tokens'])
	print '\n'

for i in range(len(sortedAnswers)):
	s = sortedAnswers[i]
	x = s[0]
	print 'Potential Answer:',
	for j in range(len(tokenized['sentences'][x[0]]['lemmas'])):
		w = tokenized['sentences'][x[0]]['lemmas'][j]
		if w.lower() not in map(lambda x:x.lower(),questionList[i]):
			print tokenized['sentences'][x[0]]['tokens'][j],
	print '\n'
