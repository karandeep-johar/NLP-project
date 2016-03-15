proc = proc1
def answerYesNo(question,answerSentences,QPObj):
    if 'BOOLEAN' in QPObj.answer_type:
        answers = []
        puncTags = ['.',',','IN','#','$','CC','SYM','-LRB-','-RRB-']
        qLemmas = [w.lower() for w in proc.parse_doc(question)['sentences'][0]['lemmas']]
            for i in range(len(answerSentences)):
                s = answerSentences[i]
                lemmas = s[2]
                posTags = proc.parse_doc(s[3])['sentences'][0]['pos']
                answer = []
                for j in range(len(lemmas)):
                    w = lemmas[j]
                    if w.lower() not in qLemmas\
                    or posTags[j] not in puncTags:
                        answer.append(s[1][j])
                    else:# Heuristic for score
                        pass
                if len(answer)>0:
                    answers.append('No')
                else:
                    answers.append('Yes')
        return answers
    else:
        return 'INVALID'