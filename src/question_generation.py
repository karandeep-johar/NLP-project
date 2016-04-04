import init

class generateQuestions:

    def __init__(self, data, n = 1):
        self.corpus = data
        self.numQues = n
        self.questions = []
        self.generate()
        # self.generate()

    def __str__(self):
        return str(self.questions)

    def getQues(self,parsed):
        questions = []
        for s in parsed['sentences']:
            pos = s['pos']
            ner = s['ner']
            tokens = s['tokens']
            tokens[-1] ="?"
            '''
            nounIndices = []
            for i in range(0, len(pos)):
                tag = pos[i]
                if tag[0:2] == 'NN':
                    nounIndices.append(i)
            '''
            for i in range(0,len(pos)):
                if pos[i][0:2] != 'NN':
                    k = i
                    break
            i = 0
            tag = pos[i]
            if tokens[i] == "It":
                questions.append('What '+' '.join(tokens[1:]))
            if tag[0:2] == 'NN':
                # TODO: Check for What questions first
                # TODO: Replace whole NP, not just the noun
                if ner[i] == 'PERSON':
                    questions.append('Who '+' '.join(tokens[k:]))
                elif ner[i] == 'LOCATION':
                    questions.append('Where '+' '.join(tokens[k:]))
                elif ner[i] == 'DATE':
                    questions.append('When '+' '.join(tokens[k:]))
                else:
                    questions.append('What '+' '.join(tokens[k:]))
            '''
            for i in nounIndices:
                if ner[i] == 'PERSON':
                    if i == 0:
                        questions.append('Who '+' '.join(tokens[1:]))
                elif ner[i] == 'LOCATION':
                    if i == 0:
                        questions.append('Where '+' '.join(tokens[1:]))
                elif ner[i] == 'DATE':
                    if i == 0:
                        questions.append('When '+' '.join(tokens[1:]))
                else:
                    if i == 0:
                        questions.append('What '+' '.join(tokens[1:]))
            '''
        return questions
    def get_questions(self):
        return self.questions
    def generate(self):
        proc = init.proc1
        pp = init.pprint.PrettyPrinter(indent=2)
        parsed = proc.parse_doc(self.corpus)
        # pp.pprint(parsed)
        self.questions = self.getQues(parsed)
