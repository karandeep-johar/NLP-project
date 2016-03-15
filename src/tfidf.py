# run using python tfidf.py
from gensim import corpora, models, similarities
from stanford_corenlp_pywrapper import CoreNLP
import sys
import pprint
from init import *
pp = pprint.PrettyPrinter(indent=2)
# CoreNLP initialization
proc = proc2



class TF_IDF(object):
    """docstring for tfidf"""
    def __init__(self, article,questions):
        self.article = article
        self.questions = questions
        
        # Tokenization
        self.tokenized = proc.parse_doc(article)

        # Extracting tokenized sentences
        sentenceList = [s['lemmas'] for s in self.tokenized['sentences']]
        questionList = [proc.parse_doc(q)['sentences'][0]['lemmas'] for q in questions]
        numSentences = len(sentenceList)

        # Generating dictionary
        self.dictionary = corpora.Dictionary(sentenceList + questionList)
        # dictionary.save('/tmp/corpDict.dict')

        # Converting corpus and questions to vector representation
        corpusVectors = [self.dictionary.doc2bow(c) for c in sentenceList]
        qBOW = [self.dictionary.doc2bow(c) for c in questionList]
        # Initializing TF-IDF model        
        self.tfidf = models.TfidfModel(corpusVectors)
        # Extracting TF-IDF of documents
        self.corpusTfidf = self.tfidf[corpusVectors]
        self.index = similarities.SparseMatrixSimilarity(self.corpusTfidf, num_features=len(self.dictionary), num_best=5)

    def getInterestingText(self,question):
        newQBOW = self.dictionary.doc2bow(proc.parse_doc(question)['sentences'][0]['lemmas'])
        answerSentences = self.index[self.tfidf[newQBOW]]
        answerSentences = sorted(answerSentences, key=lambda tup: tup[1], reverse=True)
        answerSentences = [(x[1],\
            self.tokenized['sentences'][x[0]]['tokens'],\
            self.tokenized['sentences'][x[0]]['lemmas'],\
            self.article[self.tokenized['sentences'][x[0]]['char_offsets'][0][0]:self.tokenized['sentences'][x[0]]['char_offsets'][-1][1]]
            ) for x in answerSentences]
        return answerSentences
    
    def getAnswer(self,question,answerSentences):
        potAnswers = []
        for i in range(len(answerSentences)):
            s = answerSentences[i]
            lemmas = s[2]
            answer = ''
            for j in range(len(lemmas)):
                w = lemmas[j]
                if w.lower() not in map(lambda x: x.lower(), proc.parse_doc(question)['sentences'][0]['lemmas']):
                    answer = answer+' '+s[1][j]
                else:# Heuristic for score
                    pass
            if len(answer)>0:
                potAnswers.append(answer[1:])
            else:
                potAnswers.append('')
        return potAnswers

# # Tokenization
# tokenized = proc.parse_doc(open('wiki.txt').read())
# questionList = [proc.parse_doc(q)['sentences'][0]['lemmas']
#                 for q in open('questions.txt').read().split('\n')]

# # Extracting tokenized sentences
# sentenceList = [s['lemmas'] for s in tokenized['sentences']]
# numSentences = len(sentenceList)

# # Generating dictionary
# dictionary = corpora.Dictionary(sentenceList + questionList)
# # dictionary.save('/tmp/corpDict.dict')

# # Converting corpus and questions to vector representation
# corpusVectors = [dictionary.doc2bow(c) for c in sentenceList]
# qBOW = [dictionary.doc2bow(c) for c in questionList]

# # corpora.MmCorpus.serialize('/tmp/corpVect.mm', corpusVectors)
# # dictionary = corpora.Dictionary.load('/tmp/corpDict.dict')
# # corpus = corpora.MmCorpus('/tmp/corpVect.mm')

# # Initializing TF-IDF model
# tfidf = models.TfidfModel(corpusVectors)

# # Extracting TF-IDF of documents
# corpusTfidf = tfidf[corpusVectors]
# index = similarities.SparseMatrixSimilarity(corpusTfidf, num_features=len(dictionary), num_best=5)

# # index.save('/tmp/deerwester.index')
# # index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
# sims = []
# # Similarity computation
# for q in qBOW:
#     sims.append(index[tfidf[q]])
# # pp.pprint(sims)
# sortedAnswers = []
# for answerSentences in sims:
#     answerSentences = sorted(answerSentences, key=lambda tup: tup[1], reverse=True)
#     sortedAnswers.append(answerSentences)
# # print(sortedAnswers)
# # sortedSims.filter(lambda tup:tup[0]<numSentences)
# for s in sortedAnswers:
#     for x in s:
#         print 'Potential sentence (score:%.2f' % (x[1],), '):',
#         print ' '.join(tokenized['sentences'][x[0]]['tokens'])
#     print '\n'

# # Potential Answer Generation
# for i in range(len(sortedAnswers)):
#     s = sortedAnswers[i]
#     x = s[0]
#     print 'Potential Answer:',
#     for j in range(len(tokenized['sentences'][x[0]]['lemmas'])):
#         w = tokenized['sentences'][x[0]]['lemmas'][j]
#         if w.lower() not in map(lambda x: x.lower(), questionList[i]):
#             print tokenized['sentences'][x[0]]['tokens'][j],
#     print '\n'