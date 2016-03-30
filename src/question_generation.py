import init

class generateQuestions:

    def __init__(self, data, n = 1):
        self.corpus = data
        self.numQues = n
        self.questions = []
        self.generate()

    def __str__(self):
        return self.questions

    def getWhoQuestion(self,s,pos):
        print s
        # print pos
        pass
    
    def getWhereQuestion(self,s,pos):
        pass
    
    def getWhenQuestion(self,s,pos):
        pass
    
    def getWhatQuestion(self,s,pos):
        pass

    def getQues(self,parsed):
        questions = []
        print len(parsed['sentences'])
        for s in parsed['sentences']:
            pos = s['pos']
            ner = s['ner']
            tokens = s['tokens']
            print tokens
            nounIndices = []
            for i in range(0, len(pos)):
                tag = pos[i]
                if tag[0:2] == 'NN':
                    nounIndices.append(i)
            for i in nounIndices:
                if ner[i] == 'PERSON':
                    questions.append(self.getWhoQuestion(tokens,pos))
                elif ner[i] == 'LOCATION':
                    questions.append(self.getWhereQuestion(tokens,pos))
                elif ner[i] == 'DATE':
                    questions.append(self.getWhenQuestion(tokens,pos))
                else:
                    questions.append(self.getWhatQuestion(tokens,pos))
        return questions

    def generate(self):
        proc = init.proc1
        pp = init.pprint.PrettyPrinter(indent=2)
        parsed = proc.parse_doc(self.corpus)
        # pp.pprint(parsed)
        self.questions = self.getQues(parsed)
