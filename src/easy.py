from init import *
proc = proc1
# TODO remove unicode like u'&#27713;, 
# experiment with stemmer 
# lower the tfidf score for expremely short sentences
# check low tfidf score of the answer
# to trip people up we can convert numbers to words or vice versa
# handle stupid negations
def checkDifference(answer):
    return len(answer)>0


def answerYesNo(question,answerSentences,QPObj,titleLemmasSet=set(),stopLemmasSet=set()):
    if 'BOOLEAN' in QPObj.answer_type:
        answers = []
        qLemmas = [w.lower() for w in proc.parse_doc(question)['sentences'][0]['lemmas']]
        for i in range(len(answerSentences)):
            s = answerSentences[i]
            answerLemmas = s[1]['lemmas']
            posTags = s[1]['pos']
            answer = []
            # question - answer
            answer = set(qLemmas) - \
                     set(map(lambda x:x.lower(), answerLemmas)) - \
                     set(qLemmas[0]) - \
                     titleLemmasSet - \
                     stopLemmasSet - \
                     set(puncTags)
            # for j in range(len(answerLemmas)):
            #     w = answerLemmas[j]
            #     if w.lower() not in qLemmas and posTags[j] not in puncTags:
            #         answer.append(s[1]['tokens'][j])
            #     else:# Heuristic for score
            #         pass
            print "candidate Sentence:",s, "\nanswer:", answer
            if checkDifference(answer):
                answers.append('No')
            else:
                # answer - question
                # TODO: To be improved
                if 'not' in answerLemmas and 'not' not in qLemmas:
                    answers.append('No Sure')
                else:
                    answers.append('Yes')
        if 'No Sure' in answers:
            return 'No'
        elif 'Yes' in answers:
            return 'Yes'
        else:
            return 'No'
    else:
        return 'INVALID'