from init import *
from nltk.stem.porter import *
ps = PorterStemmer()
proc = proc2
# TODO remove unicode like u'&#27713;, 
# experiment with stemmer 
# lower the tfidf score for expremely short sentences
# check low tfidf score of the answer
# to trip people up we can convert numbers to words or vice versa
# handle stupid negations
def checkDifference(answer):
    return len(answer)>0

negationCutoff = 5
exceptionSet=set(['also','like'])
# maybe neither, nor, never
negationSet=set(['no','not', "n't"])
def answerYesNo(question,answerSentences,QPObj,titleLemmasSet=set(),stopLemmasSet=set()):
    if 'BOOLEAN' in QPObj.answer_type:
        answers = []
        qLemmas = [w.lower() for w in proc.parse_doc(question)['sentences'][0]['lemmas']]
        qLemmas = [ps.stem(w) for w in qLemmas]
        stopLemmasSet = set([ps.stem(w) for w in stopLemmasSet])
        titleLemmasSet = set([ps.stem(w) for w in titleLemmasSet])
        for i in range(len(answerSentences)):
            s = answerSentences[i]
            answerLemmas = s[1]['lemmas']
            answerLemmas = [ps.stem(w) for w in answerLemmas]
            posTags = s[1]['pos']
            answer = []
            # question - answer
            answer = set(qLemmas) - \
                     set(map(lambda x:x.lower(), answerLemmas)) - \
                     set(qLemmas[0]) - \
                     titleLemmasSet - \
                     stopLemmasSet - \
                     set(puncTags) - \
                     exceptionSet
            # for j in range(len(answerLemmas)):
            #     w = answerLemmas[j]
            #     if w.lower() not in qLemmas and posTags[j] not in puncTags:
            #         answer.append(s[1]['tokens'][j])
            #     else:# Heuristic for score
            #         pass
            logger.critical("candidate Sentence:")
            logger.critical(s)
            logger.critical("\nanswer:")
            logger.critical(answer)
            if checkDifference(answer):
                answers.append('No')
            else:
                # answer - question
                # TODO: To be improved
                negFound=False
                for neg in negationSet:
                    if neg in answerLemmas and neg not in qLemmas:
                        answers.append('No Sure')
                        negFound = True
                        break
                if not negFound:
                    answers.append('Yes')
        logger.critical(answers)
        if 'No Sure' in answers[:negationCutoff]:
            return 'No.'
        elif 'Yes' in answers:
            return 'Yes.'
        else:
            return 'No.'
    else:
        return 'INVALID'