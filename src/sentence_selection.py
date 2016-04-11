import init
import nltk

class sentenceSelector:

    def __init__(self, data,k):
        self.corpus = data
        self.sentences = []
        self.needTransform = []
        self.remaining = []
        self.pickTopk(k)

    def __str__(self):
        return str(self.questions)
    
    def get_sentences(self):
        return self.sentences
        
    def get_remaining(self):
        return self.remaining

    def get_needTransform(self):
        return self.needTransform

    def pickTopk(self,k):
        paras = self.corpus.split('\n')
        for p in paras:
            parsed = init.proc2.parse_doc(p)
            count = 0
            for s in parsed[u'sentences']:
                tokens = s[u'tokens']
                sentence = ' '.join(tokens)
                # TODO: More specific constraints for transformation
                # Handle appositions
                if len(tokens) > 20:
                    self.needTransform.append(sentence)
                elif count < k:
                    count = count + 1
                    self.sentences.append(sentence)
                else:
                    self.remaining.append(sentence)
        '''
        f1 = open('needtransform.txt','w')
        f2 = open('sentences.txt','w')
        f3 = open('remaining.txt','w')
        '''
        self.needTransform = ' '.join(self.needTransform)
        self.sentences = ' '.join(self.sentences)
        self.remaining = ' '.join(self.remaining)
