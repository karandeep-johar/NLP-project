import init
import nltk

class sentenceSelector:

    def __init__(self, data,k):
        self.corpus = data
        # self.tokenized = init.proc2.parse_doc(data)
        self.sentences = []
        self.pickTopFive(k)

    def __str__(self):
        return str(self.questions)
    
    def get_sentences(self):
        return self.sentences

    def pickTopFive(self,k):
        paras = self.corpus.split('\n')
        for p in paras:
            parsed = init.proc2.parse_doc(p)
            for s in parsed[u'sentences'][0:k]:
                tokens = s[u'tokens']
                sentence = ' '.join(tokens)
                self.sentences.append(sentence)
        self.sentences = ' '.join(self.sentences)

    '''
    def generate(self):
        self.corpus = self.corpus.split('\n')
        count = 0
        val = 0
        for s in self.corpus:
            count = count+1
            words = s.split()
            if not (len(set(self.tokenized['sentences'][x[0]]['lemmas'])-set(init.puncTags))<3):
                val = val+1
                self.sentences.append(s)
        print count
        print val
    '''