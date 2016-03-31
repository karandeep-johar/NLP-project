from init import *
proc = proc1
#TODO remove unicode like u'&#27713;, piano vertical
# lower the tfidf score for expremely short sentences
#check low tfidf score of the answer, check if any of the 5 answers return a yes, remove headings
# to trip people up we can convert numbers to words or vice versa
#  handle stupid negations
# remove quotes
def answerYesNo(question,answerSentences,QPObj,titleLemmasSet=set(),stopLemmasSet=set()):
    if 'BOOLEAN' in QPObj.answer_type:
        answers = []
        puncTags = ['.',',','IN','#','$','CC','SYM','-LRB-','-RRB-']
        qLemmas = [w.lower() for w in proc.parse_doc(question)['sentences'][0]['lemmas']]
        for i in range(len(answerSentences)):
            s = answerSentences[i]
            lemmas = s[1]['lemmas']
            posTags = s[1]['pos']
            answer = []
            # question - answer
            answer = set(qLemmas) - set(map(lambda x:x.lower(), lemmas)) -set([qLemmas[0],qLemmas[-1]]) - titleLemmasSet - stopLemmasSet
            # for j in range(len(lemmas)):
            #     w = lemmas[j]
            #     if w.lower() not in qLemmas and posTags[j] not in puncTags:
            #         answer.append(s[1]['tokens'][j])
            #     else:# Heuristic for score
            #         pass
            print "candidate Sentence:",s, "\nanswer:", answer
            if len(answer)>0:
                answers.append('No')
            else:
                answers.append('Yes')
        return answers
    else:
        return 'INVALID'